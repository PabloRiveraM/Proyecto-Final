class Estudiante:
    def __init__(self, id_estudiante, nombre, nombre_contacto, relacion_contacto, 
                 telefono_contacto, datos_medicos, datos_academicos):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.nombre_contacto = nombre_contacto
        self.relacion_contacto = relacion_contacto
        self.telefono_contacto = telefono_contacto
        self.datos_medicos = datos_medicos
        self.datos_academicos = datos_academicos
        
    def actualizar_info_contacto(self, nombre_contacto, relacion_contacto, telefono_contacto):
        self.nombre_contacto = nombre_contacto
        self.relacion_contacto = relacion_contacto
        self.telefono_contacto = telefono_contacto

    def actualizar_datos_medicos(self, nuevos_datos_medicos):
        self.datos_medicos = nuevos_datos_medicos

    def actualizar_datos_academicos(self, nuevos_datos_academicos):
        self.datos_academicos = nuevos_datos_academicos