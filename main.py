from flask import Flask, render_template, redirect, request, flash, send_from_directory
import json
import ast
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import sessionmaker



engine = create_engine('mssql+pyodbc://DESKTOP-3NB93KR/cadastro?driver=ODBC+Driver+17+for+SQL+Server')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer,primary_key=True)
    nome_usuario = Column(String,nullable=False)
    senha_usuario = Column(String,nullable=False)
    

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-3NB93KR/cadastro?driver=ODBC+Driver+17+for+SQL+Server'
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

@app.route('/usuarios')
def usuarios():
    if logado == True:
        arquivo = []
        for documento in os.listdir('arquivos'):
            arquivo.append(documento)

        return render_template('usuarios.html',arquivos=arquivo)
    else:
        return redirect('/')

@app.route('/login',methods=['POST'])
def login():

    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')
    usuariosBD = session.query(Usuario).all()

    cont = 0
    for usuario in usuariosBD:
            cont+=1
            usuarioNome = usuario.nome_usuario
            usuarioSenha = usuario.senha_usuario
            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')

            if usuarioNome == nome and usuarioSenha == senha:
                logado=True
                return redirect('/usuarios')
            
            if cont >= len(usuariosBD):
               flash('Usuário inválido, tente novamente')
               return redirect('/')
            
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    novo_usuario = Usuario(nome_usuario=nome,senha_usuario=senha)
    session.add(novo_usuario)
    session.commit()
    logado = True
    flash(f'{nome} cadastrado!')

    return redirect('/adm')

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuarioParaExcluir')
    usuarioDict = ast.literal_eval(usuario)
    nome = usuarioDict['nome']
    with open('usuarios.json') as usuariosTemp:
        usuarioPy = json.load(usuariosTemp)
        for i in usuarioPy:
            if i == usuarioDict:
                usuarioPy.remove(usuarioDict)
                with open('usuarios.json','w') as usuarioAexcluir:
                    json.dump(usuarioPy,usuarioAexcluir,indent=2)

    flash(f'{nome} excluido com sucesso')
    return redirect('/adm')
    
@app.route('/upload', methods=['POST'])
def upload():
    global logado
    logado=True

    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ","-")
    arquivo.save(os.path.join('arquivos/', nome_arquivo))

    flash('ARQUIVO SALVO')


    return redirect('/adm')


   
@app.route('/download', methods=['POST'])
def download():
    nomeArquivo = request.form.get('arquivosParaDownload')

    return send_from_directory('arquivos', nomeArquivo, as_attachment=True)
   


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    Base.metadata.create_all(bind=engine)