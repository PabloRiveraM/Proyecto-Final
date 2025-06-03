class Profesor:
    def __init__(self, id_profesor, nombre, info_contacto):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.info_contacto = info_contacto

    def actualizar_info_contacto(self, nueva_info_contacto):
        self.info_contacto = nueva_info_contacto