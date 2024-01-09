# user.py
from flask import Blueprint, request, redirect, url_for, render_template, flash,jsonify
from flask_login import login_user
from flask_jwt_extended import create_access_token,create_refresh_token
from werkzeug.security import check_password_hash
from models import User
import logging
from datetime import timedelta
from cors_config import cross_origin

logging.basicConfig(level=logging.INFO)
user_info = Blueprint('user', __name__)


@user_info.route('/login', methods=['POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)  # 创建刷新令牌

            logging.info(f"用户{username}成功登录，用户ID为{user.user_id}。")
            return jsonify({'message': '登录成功', 'access_token': access_token, 'refresh_token': refresh_token, 'Username': username, "Userid": user.user_id}), 200
        else:
            logging.warning(f"{username}的登录尝试失败。")
            return jsonify({'error': '用户名或密码无效'}), 401


@user_info.route('/user/<int:user_id>', methods=['GET'])
@cross_origin()  # 允许所有域名跨源访问这个路由
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'name': user.username})  # 返回用户的 name 字段
    else:
        return jsonify({'error': 'User not found'}), 502