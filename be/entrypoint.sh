#!/bin/bash

# 設置嚴格模式
set -e

# 測試 SSH 連接
echo "Testing SSH connection..."
python3 test_ssh.py

# 啟動 Flask 應用
echo "Starting Flask application..."
exec python3 main.py
