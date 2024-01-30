

from flask import Flask, render_template, redirect, request, flash
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-JIN1HLA/teste?driver=ODBC+Driver+17+for+SQL+Server'
app.secret_key = 'joao07'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        with open('usuarios.json') as cadastrados:
            usuarios = json.load(cadastrados)

        return render_template('adm.html',usuarios=usuarios)
    if logado == False:
       return redirect('/')


@app.route('/login',methods=['POST'])
def login():

    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        cont = 0
        for usuario in usuarios:
            cont+=1

            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')

            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template('usuario.html')
            
            if cont >= len(usuarios):
               flash('Usuário inválido, tente novamente')
               return redirect('/')
            
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {"nome":nome,"senha":senha}
    ]

    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
    
    novoUsuario = usuarios + user

    with open('usuarios.json', 'w') as gravarTemp:
        json.dump(novoUsuario,gravarTemp, indent=2)

    return redirect('/adm')
    

   
   


if __name__ == "__main__":
    app.run(debug=True, port=5001)