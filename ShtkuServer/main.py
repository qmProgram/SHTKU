import sys
sys.path.append('./')
from flask import Flask
from routes.api_routes import set_routes  # 导入你自己定义的 set_routes
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
set_routes(app)  # 直接调用你自己定义的 set_routes 函数

if __name__ == '__main__':
    app.run(debug=True)
