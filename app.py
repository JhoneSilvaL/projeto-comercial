from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Página inicial'

@app.route('/cadastro')
def cadastro():
    return render_template('inicial.html')

if __name__ == '__main__':
    app.run()
