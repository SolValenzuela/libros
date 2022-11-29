from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.libro import Libro
from ..models.autor import Autor



@app.route('/libros')
def books():
    return render_template('libros.html',libros=Libro.get_all())



@app.route('/process/libros',methods=['POST'])
def procesar_libro():
    data_libro={
        "titulo":request.form['titulo'],
        "num_de_paginas":request.form['num_de_paginas']
    }
    Libro.save(data_libro)
    return redirect('/libros')


@app.route('/libros/<int:id>')
def mostrar_libros(id):
    data = {
        "id":id
    }
    return render_template('mostrar_libros.html',libro=Libro.get_by_id(data),autor_sin_favoritos=Autor.autor_sin_favoritos(data))


@app.route('/join/autor',methods=['POST'])
def join_autor():
    data = {
        'autor_id': request.form['autor_id'],
        'libro_id': request.form['libro_id']
    }
    Autor.agregar_favorito(data)
    return redirect(f"/libros/{request.form['libro_id']}")