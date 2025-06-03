class Profesor:
    def __init__(self, id_profesor, nombre, info_contacto):
        # ID único del profesor
        self.id_profesor = id_profesor
        # Nombre completo del profesor
        self.nombre = nombre
        # Información de contacto (teléfono, correo, etc.)
        self.info_contacto = info_contacto

    def actualizar_info_contacto(self, nueva_info_contacto):
        # Método para actualizar la información de contacto
        self.info_contacto = nueva_info_contacto