

from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-JIN1HLA/teste?driver=ODBC+Driver+17+for+SQL+Server'

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login():

    nome = request.form.get('nome')
    senha = request.form.get('senha')
    print(nome)
    print(senha)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, port=5001)