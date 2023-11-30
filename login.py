# login.py
from flask import Blueprint, request, redirect, url_for, render_template, flash,jsonify
from flask_login import login_user
from werkzeug.security import check_password_hash
from models import User
import logging
logging.basicConfig(level=logging.INFO)
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 尝试解析JSON数据，而不是使用表单数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            logging.info(f"User {username} logged in successfully.")
            return jsonify({'message': 'Logged in successfully'}), 200  # 发送JSON响应
        else:
            logging.warning(f"Failed login attempt for {username}.")
            return jsonify({'error': 'Invalid username or password'}), 401  # 发送错误的JSON响应

    # 如果是GET请求，则渲染登录页面
    return render_template('login.html')  # 替换为你的登录页面模板