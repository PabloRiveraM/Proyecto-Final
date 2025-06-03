class Curso:
    def __init__(self, id_curso, nombre, descripcion, id_profesor):
        self.id_curso = id_curso
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_profesor = id_profesor

    def actualizar_descripcion(self, nueva_descripcion):
        self.descripcion = nueva_descripcion

    def asignar_profesor(self, nuevo_id_profesor):
        self.id_profesor = nuevo_id_profesor