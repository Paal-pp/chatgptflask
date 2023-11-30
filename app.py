from flask import Flask ,jsonify
from flask import Flask
from models import db, User, ChatRecord
from flask_login import LoginManager, login_user
from flask_jwt_extended import JWTManager
from login import   login_blueprint
from flask_login import current_user
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://alan:Muzata901alan@192.168.1.252:3306/chatgptweb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Muzata-Merande'
app.register_blueprint(login_blueprint)
db.init_app(app)
CORS(app)
# app.py
login_manager = LoginManager(app)
login_manager.login_view = 'login.login'  # 'blueprint_name.function_name'

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



if __name__ == '__main__':
    app.run(debug=True)
