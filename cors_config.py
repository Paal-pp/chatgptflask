# cors_config.py

from flask_cors import CORS, cross_origin

def configure_cors(app):
    CORS(app,supports_credentials=True)
    # 这里可以添加更多 CORS 相关的配置
