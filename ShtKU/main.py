import re
from pymongo import MongoClient
from collections import deque
import openai
import threading
from datetime import datetime
openai.api_key = "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"
openai.api_base = "http://172.178.89.163:3001/v1"

# 连接MongoDB数据库
client = MongoClient("mongodb://SHTKU:qimengkeji147@1.15.136.115:27017/shtku")
db = client['shtku']


# 选择集合，也就是表
collection = db['Question']
evaluation_collection = db['EvaluationResults']

# 查询所有问题，不包括MongoDB的内部_id字段
questions = collection.find({}, {'_id': 0})

# 初始化一个待问队列
questions_queue = deque()
# 将问题添加到待问队列
for question in questions:
    questions_queue.append(question)

evaluation_results = []
def process_question():
    while questions_queue:
        current_question = questions_queue.popleft()
        extracted_id  = current_question['id']
        extracted_question = current_question['question']
        extracted_answers = current_question['answers']
        extracted_rightanswer = current_question['rightanswer'] # 这里只是一个示例
        score =0

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "I provide you with a question, the question has corresponding options, you only need to answer the corresponding options, such as A, B, do not need to have any extra answers, here are the questions and options. Remember that your answer can only be a letter option."},
                {"role": "user", "content": str(extracted_question)},
                {"role": "user", "content": str(extracted_answers)}
            ]
        )
        completion_output = completion.choices[0].message.content
        match = re.search(r'[A-Z]', completion_output)

        if match:
            first_capital_letter = match.group(0)
        else:
            first_capital_letter = "未获得有效答案"

        if extracted_rightanswer== first_capital_letter:
            score=1
        else:
            score=0
        print( str(extracted_id),str(extracted_question), str(extracted_answers) ,first_capital_letter,score)
        result = {
            'question_id': str(extracted_id),
            'question_content': str(extracted_question),
            'question_answers': extracted_answers,
            'model_answer': first_capital_letter,
            'score': score
        }
        evaluation_results.append(result)

# 设定一个最大和最小线程数
max_threads = 10
min_threads = 1

# 根据队列长度动态设置线程数量
queue_length = len(questions_queue)
threads_to_create = min(max_threads, max(min_threads, queue_length))

threads = []  # 创建一个线程列表

# 启动线程并将它们添加到线程列表中
for i in range(threads_to_create):
    t = threading.Thread(target=process_question)
    threads.append(t)
    t.start()

# 使用线程列表来等待每个线程完成
for t in threads:
    t.join()

# 插入评估结果到新的表中
evaluation_data = {
    'evaluator': 'gpt-3.5-turbo',  # 请替换为真实的测评人姓名
    'model': 'gpt-3.5-turbo',
    'evaluation_time': datetime.now(),
    'evaluation_results': evaluation_results
}
evaluation_collection.insert_one(evaluation_data)
