from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import autor


class Libro:
    

    def __init__(self,data):
        self.id = data['id']
        self.titulo= data['titulo']
        self.num_de_paginas=data['num_de_paginas']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.autores_y_favoritos = []

        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO libros (titulo,num_de_paginas,created_at,updated_at) VALUES (%(titulo)s,(%(num_de_paginas)s),NOW(),NOW())"
        return connectToMySQL('libros').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM libros;"
        libros =  connectToMySQL('libros').query_db(query)
        libro =[]
        for b in libros:
            libro.append(cls(b))
        return libro
    

    @classmethod
    def libros_sin_favoritos(cls,data):
        query = "SELECT * FROM libros WHERE libros.id NOT IN ( SELECT libro_id FROM favoritos WHERE autor_id = %(id)s );"
        results = connectToMySQL('libros').query_db(query,data)
        libros = []
        for libro in results:
            libros.append(cls(libro))
        print(libros)
        return libros
    


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM libros LEFT JOIN favoritos ON libros.id = favoritos.libro_id LEFT JOIN autores ON autores.id = favoritos.autor_id WHERE libros.id = %(id)s;"
        results = connectToMySQL('libros').query_db(query,data)

        libro = cls(results[0])

        for row in results:
            if row['autores.id'] == None:
                break
            data = {
                "id": row['autores.id'],
                "nombre": row['nombre'],
                "created_at": row['autores.created_at'],
                "updated_at": row['autores.updated_at']
            }
            libro.autores_y_favoritos.append(autor.Autor(data))
        return libro