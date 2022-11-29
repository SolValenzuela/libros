from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.autor import Autor
from ..models.libro import Libro



@app.route('/')
def ruta_inicio():
    return redirect('/autores')


@app.route('/process' ,methods=['POST'])
def procesar_autor():
    data={
        "nombre":request.form['nombre']
    }
    autor=Autor.save(data)
    return redirect ('/autores')


@app.route('/autores')
def todos_los_autores():
    autores=Autor.get_all()
    return render_template('autores.html',autores=autores)



@app.route('/autores/<int:id>')
def mostrar_autor(id):
    data = {
        "id": id
    }
    autor=Autor.get_by_id(data)
    libros_sin_favoritos=Libro.libros_sin_favoritos(data)
    
    return render_template('mostrar_autores.html',autor=autor,libros_sin_favoritos=libros_sin_favoritos)



@app.route('/join/libro',methods=['POST'])
def join_libro():
    data = {
        'autor_id': request.form['autor_id'],
        'libro_id': request.form['libro_id']
    }
    Autor.agregar_favorito(data)
    return redirect(f"/autores/{request.form['autor_id']}")


