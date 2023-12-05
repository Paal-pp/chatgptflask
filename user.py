# user.py
from flask import Blueprint, request, redirect, url_for, render_template, flash,jsonify
from flask_login import login_user
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import User
import logging
from datetime import timedelta
logging.basicConfig(level=logging.INFO)
user_info = Blueprint('user', __name__)

@user_info.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 尝试解析JSON数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            # 用户验证成功，创建JWT令牌
            access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(hours=24))

            logging.info(f"User {username} User {user.user_id} logged in successfully.")
            return jsonify({'message': 'Logged in successfully', 'access_token': access_token,'Username':username,"Userid":user.user_id}), 200
        else:
            logging.warning(f"Failed login attempt for {username}.")
            return jsonify({'error': 'Invalid username or password'}), 401


@user_info.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'name': user.username})  # 返回用户的 name 字段
    else:
        return jsonify({'error': 'User not found'}), 502