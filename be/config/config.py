import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Config:
    MINIKUBE_VM_IP = os.getenv('MINIKUBE_VM_IP', '10.140.0.14')
    MINIKUBE_VM_USERNAME = os.getenv('MINIKUBE_VM_USERNAME', 'alan_wang')
    MINIKUBE_SSH_KEY_PATH = os.getenv('MINIKUBE_SSH_KEY_PATH', '/home/alan_wang/.ssh/id_rsa')

    # MongoDB 配置
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")

    _settings_cache = None

    @staticmethod
    def get_client():
        try:
            client = MongoClient(Config.MONGO_URI)
            # 嘗試從數據庫中執行一次操作以確認連接
            client.admin.command('ping')
            logging.info("成功連接到 MongoDB")
            return client
        except Exception as e:
            logging.error(f"連接到 MongoDB 失敗: {e}")
            raise e
        
    @classmethod
    def get_settings_from_db(cls):
        client = cls.get_client()
        db = client['it']
        collection = db['settings']
        setting = collection.find_one()
        if setting:
            return setting
        return None
    
    @classmethod
    def get_operation_logs_from_db(cls):
        client = cls.get_client()
        db = client['it']
        collection = db['operation_logs']
        return collection

    @classmethod
    def refresh_settings_cache(cls):
        cls._settings_cache = cls.get_settings_from_db()

    @classmethod
    def get_cloudflare_api_key(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('cloudflareApiKey') if cls._settings_cache else None

    @classmethod
    def get_cloudflare_email(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('cloudflareEmail') if cls._settings_cache else None

    @classmethod
    def get_telegram_bot_token(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('telegramBotToken') if cls._settings_cache else None

    @classmethod
    def get_telegram_chat_id(cls):
        if cls._settings_cache is None:
            cls.refresh_settings_cache()
        return cls._settings_cache.get('telegramChatId') if cls._settings_cache else None


def get_client():
    return Config.get_client()

def get_secret_key():
    return Config.SECRET_KEY
