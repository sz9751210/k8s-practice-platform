#!/bin/sh

# 獲取 Minikube IP 地址
MINIKUBE_IP=${MINIKUBE_IP}

# 動態修改 kubeconfig 文件中的 server 欄位
sed -i "s#server: https://.*:8443#server: https://${MINIKUBE_IP}:8443#g" /root/.kube/config

# 確保 Minikube 證書文件的路徑正確
sed -i "s#/home/alan_wang/.minikube#/root/.minikube#g" /root/.kube/config

# 執行傳入的命令
exec "$@"
