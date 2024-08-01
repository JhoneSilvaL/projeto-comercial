from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Página inicial'

@app.route('/home')
def home():
    return 'Seja bem vindo'

if __name__ == '__main__':
    app.run()
