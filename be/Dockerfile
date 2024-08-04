# 使用官方的 Python 基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 複製應用程式碼到工作目錄
COPY . .

# 添加 entrypoint.sh 並設置為可執行
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 暴露應用的運行端口
EXPOSE 9090

# ENTRYPOINT ["/entrypoint.sh"]
ENTRYPOINT ["python3", "main.py"]
# 啟動應用
# CMD ["python", "main.py"]
