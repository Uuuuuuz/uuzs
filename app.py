from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # 启用所有来源的CORS

# 替换为你的OpenAI API密钥
OPENAI_API_KEY = 'sk-oeiTkhAycevSAOxB5dC03b21183e4909A30e5a1b85AaC159'  # 请确保把这里替换为你的实际 API 密钥
OPENAI_API_URL = 'https://api.7xnn.cn/v1/chat/completions'  # 应该使用正确的OpenAI API端点

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'reply': '请输入您的问题'}), 400

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}',
        }
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': user_message}],
            'temperature': 0.7,
        }
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # 确保捕获HTTP错误
        data = response.json()
        ai_reply = data['choices'][0]['message']['content'].strip()
        return jsonify({'reply': ai_reply})
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return jsonify({'reply': '服务器返回了一个错误，请稍后再试'}), 500
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return jsonify({'reply': '连接错误，请检查网络连接'}), 500
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return jsonify({'reply': '请求超时，请稍后再试'}), 500
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
        return jsonify({'reply': '对不起，发生了一个错误，请稍后再试'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)  # 确保应用在5003端口运行