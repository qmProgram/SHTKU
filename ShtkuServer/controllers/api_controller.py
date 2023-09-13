from models.db_config import db
from flask import jsonify, request
from collections import deque
import threading
from datetime import datetime

def get_records1():
    collection = db['Question']
    records = []
    for doc in collection.find():
        records.append(str(doc))
    return jsonify({'status': 'success', 'data': records})

def show_records():
    collection = db['EvaluationResults']
    records = []
    for doc in collection.find():
        records.append(str(doc))
    return jsonify({'status': 'success', 'data': records})
# 获取所有问题
def fetch_all_questions():
    collection = db['Question']
    records = []
    for doc in collection.find({}, {'_id': 0}):
        records.append(doc)
    return jsonify({'status': 'success', 'data': records})
# 获取所有评估结果
def fetch_all_evaluation_results():
    collection = db['EvaluationResults']
    records = []
    for doc in collection.find({}, {'_id': 0}):
        records.append(doc)
    return jsonify({'status': 'success', 'data': records})
# 添加或更新问题记录
def add_or_update_question_records():
    data = request.json
    forms = data.get('forms')

    if forms is None:
        return jsonify({'status': 'error', 'message': '缺少必要的字段'}), 400

    collection = db['Question']
    counter_collection = db['Counter']

    # 获取当前的最大ID值
    counter = counter_collection.find_one({"name": "question_id"})
    if counter is None:
        current_max_id = 0
        counter_collection.insert_one({"name": "question_id", "value": current_max_id})
    else:
        current_max_id = counter["value"]

    for form in forms:
        form_id = form.get('id')
        question = form.get('question')
        answers = form.get('answers')
        rightanswer = form.get('rightanswer')

        if not all([question, answers]):
            return jsonify({'status': 'error', 'message': '某个字段不存在'}), 400

        # 根据ID检查是否存在该问题
        existing_record = collection.find_one({'id': form_id})

        # 如果存在此ID，则进行更新
        if existing_record:
            try:
                collection.update_one({'id': form_id}, {"$set": {'question': question, 'answers': answers, "rightanswer": rightanswer}})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500
        # 如果该ID不存在，则进行插入
        else:
            # 自增ID
            current_max_id += 1
            try:
                collection.insert_one({'id': current_max_id, 'question': question, 'answers': answers, "rightanswer": rightanswer})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500

    # 更新最大ID值
    counter_collection.update_one({"name": "question_id"}, {"$set": {"value": current_max_id}})

    return jsonify({'status': 'success', 'message': '操作成功完成'}), 201
# 评估答案
def evaluate_answers():
    try:
        data = request.json  # 获取前端发送的数据
        form_data = data.get('forms', {})

        evaluator_name = form_data.get('evaluator', '')
        Hquestions = form_data.get('questions', [])

        collection1 = db['HumanEvaluation']

        # 查询是否存在相同的测评人
        existing_record = collection1.find_one({'evaluator': evaluator_name})

        if existing_record:
            # 如果测评人已存在，更新测评内容
            collection1.update_one({'evaluator': evaluator_name}, {'$set': {'questions': Hquestions}})
            message = '测评内容已更新'
        else:
            # 如果测评人不存在，插入新的记录
            new_record = {'evaluator': evaluator_name, 'questions': Hquestions}
            inserted_id = collection1.insert_one(new_record).inserted_id
            message = '新记录已添加'

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
                matching_Hquestion = next((item for item in Hquestions if item['id'] == extracted_id), None)
                print(matching_Hquestion['answer'])
                human_answer = matching_Hquestion['answer']
                score = 0
                if extracted_rightanswer==human_answer:
                    score=1
                else:
                    score=0
                print( str(extracted_id),str(extracted_question), str(extracted_answers) ,human_answer,score)
                result = {
                    'question_id': str(extracted_id),
                    'question_content': str(extracted_question),
                    'question_answers': extracted_answers,
                    'model_answer': human_answer,
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
            'evaluator': evaluator_name,  # 请替换为真实的测评人姓名
            'model': evaluator_name,
            'evaluation_time': datetime.now(),
            'evaluation_results': evaluation_results
        }
        evaluation_collection.insert_one(evaluation_data)
        message += "评测结果已提交"
        return jsonify({'status': 'success', 'message': message}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
# 删除所有问题
def delete_all_questions():
    collection = db['Question']
    collection.delete_many({})
    return jsonify({'status': 'success', 'message': '所有记录已删除'}), 200
# 通过ID删除特定问题
def delete_question_by_id():
    form_id = request.json.get('id')
    if form_id is None:
        return jsonify({'status': 'error', 'message': '缺少必要的 id 字段'}), 400

    collection = db['Question']
    result = collection.delete_one({'id': form_id})

    if result.deleted_count > 0:
        return jsonify({'status': 'success', 'message': f'记录 {form_id} 已删除'}), 200
    else:
        return jsonify({'status': 'error', 'message': f'找不到 id 为 {form_id} 的记录'}), 404
