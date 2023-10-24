from pymongo import MongoClient
import json

# 连接MongoDB数据库
client = MongoClient("mongodb://SHTKU:qimengkeji147@1.15.136.115:27017/shtku")
db = client['shtku']

# 选择集合，也就是表
collection = db['Question']

# 删除原有所有数据（直接删除该集合）
collection.drop()

# 读取TXT文件中的JSON数据
with open("question.txt", "r", encoding="utf-8") as f:
    forms = json.load(f)  # 假设你的TXT文件是一个合法的JSON格式

# 从1开始作为新数据的ID
current_max_id = 1

# 循环遍历每个问题并插入数据库
for form in forms:
    question = form.get('question')
    answers = form.get('answers')
    rightanswer = form.get('rightanswer')

    if not all([question, answers, rightanswer]):
        print(f"Skipping due to missing fields: {form}")
        continue

    # 自增ID
    form['id'] = current_max_id
    current_max_id += 1

    try:
        # 插入一条记录
        collection.insert_one(form)
        print(f"Successfully inserted question with ID {form['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

print("Finished inserting all questions.")
