import re
from pymongo import MongoClient
import openai
from datetime import datetime
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

# 设置OpenAI API相关信息（注意，不推荐在代码中明文存储API密钥）
openai.api_key =  os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("VITE_API_BASE_URL")

# 连接MongoDB数据库
client = MongoClient(os.getenv("MONGO_URI"))
db = client['shtku']
collection = db['Question']
evaluation_collection = db['EvaluationResults']

# 从数据库读取问题
questions = collection.find({}, {'_id': 0})

model = "chatglm_pro"
# 初始化评估结果列表
evaluation_results = []

# 处理单个问题的函数
def process_question(current_question):
    # 从当前问题中提取信息
    extracted_id = current_question['id']
    extracted_question = current_question['question']
    extracted_answers = current_question['answers']
    extracted_rightanswer = current_question['rightanswer']
    print(extracted_question)

    try:
        # 使用OpenAI API获取模型的答案
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": "I provide you with a question, the question has corresponding options, you only need to answer the corresponding options, such as A, B, do not need to have any extra answers, here are the questions and options. Remember that your answer can only be a letter option."},
                {"role": "user", "content": str(extracted_question)},
                {"role": "user", "content": str(extracted_answers)}
            ]
        )

        # 解析模型的输出
        completion_output = completion.choices[0].message.content
        print(completion.choices[0].message.content)
        match = re.search(r'[A-Z]', completion_output)
        first_capital_letter = match.group(0) if match else "未获得有效答案"

        # 评分
        score = 1 if extracted_rightanswer == first_capital_letter else 0

        # 将结果保存到评估结果列表
        result = {
            'question_id': str(extracted_id),
            'question_content': str(extracted_question),
            'question_answers': extracted_answers,
            'model_answer': first_capital_letter,
            'score': score
        }

        evaluation_results.append(result)

    except Exception as e:
        print(f"An error occurred: {e}")

# 使用for循环处理每个问题
for question in questions:
    process_question(question)

# 保存评估结果到MongoDB
evaluation_data = {
    'evaluator': model,
    'model': model,
    'evaluation_time': datetime.now(),
    'evaluation_results': evaluation_results
}

try:
    evaluation_collection.insert_one(evaluation_data)
except Exception as e:
    print(f"Database Insertion Error: {e}")
