from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrarcidade')
def cadastrarcidade():
    return render_template('inicial.html')

@app.route('/resultado')
def resultado():
    return render_template('resultadocadastro.html')






if __name__ == '__main__':
    app.run()
