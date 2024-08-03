from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Página inicial'

@app.route('/cadastro')
def cadastro():
    return render_template('cadastrarcidade.html')

@app.route('/cadastrarcidade')
def cadastrarcidade():
    return render_template('inicial.html')

@app.route('/resultado')
def resultado():
    return render_template('resultadocadastro.html')






if __name__ == '__main__':
    app.run()
