from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import libro


class Autor:
    
    def __init__(self,data):
        self.id = data['id']
        self.nombre= data['nombre']
        self.libros_favoritos = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.libros_favoritos=[]


    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO autores (nombre,created_at,updated_at) VALUES (%(nombre)s,NOW(),NOW())"
        return connectToMySQL('libros').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM autores;"
        autores =  connectToMySQL('libros').query_db(query)
        autor =[]
        for b in autores:
            autor.append(cls(b))
        return autor
    

    @classmethod
    def autor_sin_favoritos(cls,data):
        query = "SELECT * FROM autores WHERE autores.id NOT IN ( SELECT autor_id FROM favoritos WHERE libro_id = %(id)s );"
        autores = []
        results = connectToMySQL('libros').query_db(query,data)
        for autor in results:
            autores.append(cls(autor))
        return autores

    @classmethod
    def agregar_favorito(cls,data):
        query = "INSERT INTO favoritos (autor_id,libro_id) VALUES (%(autor_id)s,%(libro_id)s);"
        return connectToMySQL('libros').query_db(query,data)
    


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM autores LEFT JOIN favoritos ON autores.id = favoritos.autor_id LEFT JOIN libros ON libros.id = favoritos.libro_id WHERE autores.id = %(id)s;"
        results = connectToMySQL('libros').query_db(query,data)
        
        autor = cls(results[0])
        # autor=Autor(info_autor)
        
        for dato in results:
            # si no hay favoritos
            if dato['libros.id'] == None:
                break

            dato = {
                "id": dato['libros.id'],
                "titulo": dato['titulo'],
                "num_de_paginas": dato['num_de_paginas'],
                "created_at": dato['libros.created_at'],
                "updated_at": dato['libros.updated_at']
            }
            autor.libros_favoritos.append(libro.Libro(dato))
        return autor
    