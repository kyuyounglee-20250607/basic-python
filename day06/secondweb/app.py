from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    user = request.form['username']
    return render_template('result.html', name=user)

if __name__ == '__main__':
    app.run(debug=True)
