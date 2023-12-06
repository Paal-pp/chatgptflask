from flask import Flask ,jsonify
from flask import Flask
from models import db, User, ChatRecord
from flask_login import LoginManager, login_user
from flask_jwt_extended import JWTManager
from user import   user_info
from flask_login import current_user
from flask_cors import CORS ,cross_origin
from chatapi import chat_api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://alan:Muzata901alan@192.168.1.252:3306/chatgptweb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Muzata-Merande'
app.register_blueprint(user_info)
app.register_blueprint(chat_api, url_prefix='/api')
db.init_app(app)
jwt = JWTManager(app)
CORS(app)
# app.py
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def hello_world():  # put application's code here
    if current_user.is_authenticated:
        print("paal")
        # 显示用户相关信息
    else:
        print("test")
        # 显示登录链接
    return 'Hello World!'

@app.route('/test_connection')
def test_connection():
    try:
        # 尝试执行一个简单的数据库查询
        users_count = User.query.count()
        chatrecord =ChatRecord.query.count()
        return jsonify({"success": True, "users_count": users_count,"chatrecord":chatrecord})
    except Exception as e:
        # 如果有异常，返回错误信息
        return jsonify({"success": False, "error": str(e)})



"""
令牌过期
当令牌过期时，你可以要求用户重新登录来获取新的令牌。
"""
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has expired, please log in again."}), 401

"""
无效的令牌
如果收到的令牌无效（例如，被篡改），你可以返回错误消息。
"""
@jwt.invalid_token_loader
def invalid_token_callback(error):  # Callback function receives the error message as an argument
    return jsonify({"msg": "Invalid token.", "error": error}), 422

"""
未提供令牌
如果请求没有提供JWT令牌，你可以定义一个回调函数来处理这种情况
"""
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"msg": "Token is missing.", "error": error}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
