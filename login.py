# login.py
from flask import Blueprint, request, redirect, url_for, render_template, flash,jsonify
from flask_login import login_user
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import User
import logging
from datetime import timedelta
logging.basicConfig(level=logging.INFO)
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 尝试解析JSON数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            # 用户验证成功，创建JWT令牌
            access_token = create_access_token(identity=username, expires_delta=timedelta(hours=24))

            logging.info(f"User {username} logged in successfully.")
            return jsonify({'message': 'Logged in successfully', 'access_token': access_token}), 200
        else:
            logging.warning(f"Failed login attempt for {username}.")
            return jsonify({'error': 'Invalid username or password'}), 401

    # 如果是GET请求，则渲染登录页面
    return render_template('login.html')