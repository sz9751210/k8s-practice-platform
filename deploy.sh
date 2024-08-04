#!/bin/bash

# 獲取 Minikube IP 地址
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: ${MINIKUBE_IP}"

# 更新 docker-compose.yml 文件中的 MINIKUBE_IP 環境變量
sed -i "s/MINIKUBE_IP_PLACEHOLDER/${MINIKUBE_IP}/g" docker-compose.yaml

# 啟動 Docker Compose
docker-compose up --build
