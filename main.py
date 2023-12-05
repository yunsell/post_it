from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

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
    print(req['model'])
    print(req['messages'])
    client = OpenAI(api_key="YOUR_API_KEY")

    completion = client.chat.completions.create(
        model=req['model'],
        messages=req['messages'],
    )

    print("chatGPT : ", completion.choices[0].message.content)

    return completion.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)