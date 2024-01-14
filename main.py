from flask import Flask, render_template, request
from openai import OpenAI
import pymysql
from datetime import datetime
from config import api_key

app = Flask(__name__)
api_key = api_key

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    req = request.get_json()

    # DB 연결 설정
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "1234"
    DB_NAME = "chatgpt"

    # DB 연결 객체 생성
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

    # 데이터베이스 커서 생성
    cursor = conn.cursor()

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model=req['model'],
        messages=req['messages'],
    )

    print("chatGPT : ", completion.choices[0].message.content)

    # POST 요청에서 사용자 정보 추출
    model = req['model']
    prompt = req['prompt']
    user_text = req['messages']
    gpt_text = completion.choices[0].message.content
    created_at = datetime.now()

    # SQL 쿼리 실행
    sql = "INSERT INTO chat_log (model, prompt, user_text, gpt_text, created_at) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (str(model), str(prompt), str(user_text), str(gpt_text), str(created_at)))

    # 변경사항을 커밋
    conn.commit()

    return completion.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)