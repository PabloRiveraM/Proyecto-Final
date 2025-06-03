class AsignacionCurso:
    def __init__(self, id_asignacion, id_estudiante, id_curso, fecha_asignacion, estado="Activo"):
        self.id_asignacion = id_asignacion
        self.id_estudiante = id_estudiante
        self.id_curso = id_curso
        self.fecha_asignacion = fecha_asignacion
        self.estado = estado
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado