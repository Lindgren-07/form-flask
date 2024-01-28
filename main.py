

from flask import Flask, render_template, redirect, request, flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-JIN1HLA/teste?driver=ODBC+Driver+17+for+SQL+Server'
app.secret_key = 'joao07'

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login():

    nome = request.form.get('nome')
    senha = request.form.get('senha')
   
    if nome == 'joao' and senha == '123':
        return render_template('usuario.html')
    else:
        flash('Usuário inválido, tente novamente')
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=5001)