from flask import Blueprint, jsonify, request
from models import ChatSession, ChatRecord,User
from models import db
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity  # 假设使用 flask_jwt_extended
from app import CORS,cross_origin
import json,requests

chat_api = Blueprint('chat_api', __name__)


"""
获取历史会话信息
"""
@chat_api.route('/sessions/<int:user_id>', methods=['GET'])
@jwt_required()  # 需要JWT令牌认证
def get_chat_sessions(user_id):
    try:
        # 从JWT令牌中获取当前用户ID
        current_user_id = get_jwt_identity()

        # 检查请求的user_id是否与当前用户ID匹配
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # 从数据库中获取该用户的所有对话会话
        sessions = ChatSession.query.filter_by(user_id=user_id).all()

        # 将每个会话转换为字典格式
        sessions_data = [{
            'session_id': session.session_id,
            'title': session.tittle,
            'last_updated': session.last_updated.isoformat()
        } for session in sessions]
        print(sessions_data)
        # 返回包含会话数据的JSON响应
        return jsonify(sessions_data), 200

    except Exception as e:
        # 在出错时返回错误信息
        return jsonify({'error': str(e)}), 500



"""
获取聊天历史记录 分页
"""

@chat_api.route('/history/<string:session_id>/<int:user_id>', methods=['GET'])
@jwt_required()
def get_chat_history(session_id, user_id):
    try:
        # 从JWT令牌中获取当前用户ID
        current_user_id = get_jwt_identity()
        # 检查请求的user_id是否与当前用户ID匹配
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403

        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)

        # 从数据库中获取指定session_id的聊天记录，按时间降序
        pagination = ChatRecord.query.filter_by(session_id=session_id) \
            .order_by(ChatRecord.timestamp.asc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

        records = pagination.items

        # 将每条记录转换为字典格式
        records_data = [{
            'message': record.message,
            'response': record.response,
            'timestamp': record.timestamp.isoformat()
        } for record in records]

        # 返回包含聊天记录数据的JSON响应，以及分页信息
        return jsonify({
            'records': records_data,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200

    except Exception as e:
        # 在出错时返回错误信息
        return jsonify({'error': str(e)}), 500


"""
创建新的会话信息
"""
@chat_api.route('/chat/session/create', methods=['POST'])
@jwt_required()
def create_chat_session():
    try:
        # 解析请求体中的数据（例如：用户ID）
        data = request.json
        user_id = data.get('user_id')

        # 验证用户ID是否提供
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        # 验证用户ID是否存在于数据库中
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # 生成一个新的session_id
        new_session_id = str(uuid.uuid4())

        # 创建新的ChatSession对象，并传递user_id和其他必要信息
        new_session = ChatSession(session_id=new_session_id, user_id=user_id,tittle="Newchat")

        # 将新会话添加到数据库
        db.session.add(new_session)
        db.session.commit()

        # 返回新的session_id
        return jsonify({'session_id': new_session_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""
发送消息
"""
@chat_api.route('/chat/sendmessage', methods=['POST'])
@jwt_required()
def sendmessage():
    try:
        data =request.json
        user_id = data.get('user_id')
        message = data.get('message')
        session_id = data.get('session_id')

        # 验证数据的有效性
        if not user_id or not message or not session_id:
            return jsonify({"error": "Missing user_id, message, or session_id"}), 400

        response = request_api(message)

        # 创建新的聊天记录
        new_chat_record = ChatRecord(
            user_id=user_id,
            message=message,
            response =response,
            session_id=session_id
        )

        # 保存记录到数据库
        db.session.add(new_chat_record)
        db.session.commit()

        # 返回成功响应
        return jsonify({"message": "Message sent successfully", "message_id": new_chat_record.id}), 201

    except Exception as e:
        return jsonify({"error":str(e)}),500



    pass

def request_api(message):
    url = "http://101.36.98.230:4396/chat"

    payload = json.dumps({
        "message": message
    })
    response = requests.request("POST", url, data=payload)
    chat_requests =response.json()['message']
    return chat_requests