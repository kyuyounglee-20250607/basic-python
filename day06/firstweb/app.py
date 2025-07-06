from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return '''<h1>안녕하세요!</h1> 
    <p><h2>Flask 웹사이트입니다.</h2></p>'''

@app.route('/about')
def about():
    return "이 페이지는 소개 페이지입니다."

@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
