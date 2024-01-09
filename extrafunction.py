import json
import requests
import tiktoken
from cryptography.fernet import Fernet


def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)


def get_latest_key():
    config = load_config()
    encryption_keys = config['encryption_key']
    # 获取最大的版本号
    latest_version = max(encryption_keys.keys(), key=int)
    # 返回对应版本的密钥
    return encryption_keys[latest_version]


def request_api(message, model):
    url = "http://101.36.98.230:4396/chat"
    print(message)
    payload = json.dumps({
        "message": message,
        "model": model,
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    # 检查响应状态码
    if response.status_code != 200:
        # 处理错误情况，例如打印错误信息或抛出异常
        print(f"Error: Received status code {response.status_code}")
        return None

    try:
        chat_response = response.json()['message']
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON.")
        return None
    except KeyError:
        print("Error: 'message' not found in response.")
        return None

    return chat_response


def aes_encryption(*args, **kwargs):
        for arg in args:
            if isinstance(arg, dict) and "message" in arg and "response" in arg:
                print("找到了一个包含 'message' 和 'response' 的字典")
                # 进行相应处理
            else:
                print("参数不是包含所需键的字典")

        for key, value in kwargs.items():
            if isinstance(value, dict) and "message" in value and "response" in value:
                message = value['message']
                response = value["response"]

                key = get_latest_key()
                cipher_suite = Fernet(key)

                message_encode = cipher_suite.encrypt(message.encode())
                response_encode = cipher_suite.encrypt(response.encode())

                response_message_ditct = {"message": message_encode, "response": response_encode}
                return response_message_ditct
                # 进行相应处理
            else:
                print(f"关键字参数 {key} 不是包含所需键的字典")




def aes_decode(*args, **kwargs):
    pass
