# Shtku 项目

## 简介

这是一个关于 Shtku 项目的简单介绍。这个项目包括前端、后端，以及模型测评。

## 环境设置

### 安装依赖

运行下面的命令以安装所需的依赖：


npm install
pip install -r requirements.txt


### 配置文件

复制 `.env.example` 到 `.env`，然后根据需要进行设置：

- `VITE_API_BASE_URL`: 用于指定 API 的基础 URL。
- `OPENAI_API_KEY`: 用于 OpenAI API 的访问密钥。
- `MONGO_URI`: MongoDB 数据库的连接 URI。

## 启动项目

### 启动前端

运行以下命令以启动前端：


npm run dev


### 启动后端

运行以下命令以启动后端：


cd ShtkuServer
python main.py


## 模型测评

运行以下命令以进行模型测评：


cd LLM ShtKU
python main.py


## 更多信息

