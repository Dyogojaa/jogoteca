import time
from jogoteca import db, app
from helpers import deleta_arquivo, recupera_imagem
from flask import render_template, request, redirect,session,flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from models import Jogo

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route("/") #Começo da Renderização da Pagina HTML, ocorreu um erro nos testes ao colocar a Classe Após a Definição da Rota
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo="Catálago de Jogos", jogos=lista)

@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for('login', proxima=url_for("novo")))
    return render_template("novo.html", titulo="Novo Jogo")

@app.route("/criar", methods=["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for("index"))


@app.route("/editar/<int:id>")
def editar(id):
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for('login', proxima=url_for("editar")))
    jogo = jogo_dao.busca_por_id(id)
    capa_jogo = recupera_imagem(id) # f'capa{jogo.id}.jpg'
    return render_template("editar.html", titulo="Editando Jogo", jogo=jogo, capa_jogo=capa_jogo)

@app.route("/atualizar", methods=["POST",])
def atualizar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo( nome, categoria, console, id = request.form["id"])
    jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for("index"))


@app.route("/deletar/<int:id>")
def deletar(id):
    jogo_dao.deletar(id)
    flash("O jogo foi removido com sucesso!")
    return redirect(url_for("index"))

@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar", methods=["POST",])
def autenticar():

    usuario = usuario_dao.buscar_por_id(request.form["usuario"])
    if usuario:
        if usuario.senha == request.form["senha"]:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + " logou com sucesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
    else:
        flash("Não logado, tente novamente!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash("Nenhum usuário Logado!")
    return redirect(url_for("index"))


@app.route("/upload/<nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory('upload', nome_arquivo)
