# 使用官方的 Python 映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製應用所需的文件
COPY requirements.txt requirements.txt
COPY app app
COPY config.py config.py

# 安裝依賴
RUN pip install -r requirements.txt

# 設置環境變量以便 Flask 正確運行
ENV FLASK_APP=app
ENV FLASK_ENV=development

# 暴露 Flask 的默認端口
EXPOSE 5000

# 啟動應用
CMD ["flask", "run", "--host=0.0.0.0"]
