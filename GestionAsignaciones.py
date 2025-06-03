from AsignacionCurso import AsignacionCurso
from datetime import datetime

class GestionAsignaciones:
    def __init__(self, conexion):
        self.conexion = conexion
    
    def listar_asignaciones(self):
        try:
            cursor = self.conexion.obtener_cursor()
            cursor.execute("""
                SELECT a.id_asignacion, a.id_estudiante, a.id_curso, a.fecha_asignacion, a.estado,
                       e.nombre as nombre_estudiante, c.nombre as nombre_curso, p.nombre as nombre_profesor
                FROM asignaciones a
                JOIN estudiantes e ON a.id_estudiante = e.id_estudiante
                JOIN cursos c ON a.id_curso = c.id_curso
                JOIN profesores p ON c.id_profesor = p.id_profesor
            """)
            rows = cursor.fetchall()
            asignaciones = []
            for row in rows:
                asignacion = {
                    'id_asignacion': row[0],
                    'id_estudiante': row[1],
                    'id_curso': row[2],
                    'fecha_asignacion': row[3],
                    'estado': row[4],
                    'nombre_estudiante': row[5],
                    'nombre_curso': row[6],
                    'nombre_profesor': row[7]
                }
                asignaciones.append(asignacion)
            cursor.close()
            return asignaciones
        except Exception as e:
            print(f"Error al listar asignaciones: {e}")
            return []
    
    def asignar_curso(self, id_estudiante, id_curso):
        try:
            cursor = self.conexion.obtener_cursor()
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                """INSERT INTO asignaciones 
                (id_estudiante, id_curso, fecha_asignacion, estado) 
                VALUES (%s, %s, %s, %s)""",
                (id_estudiante, id_curso, fecha_actual, "Activo")
            )
            self.conexion.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al asignar curso: {e}")
            return False
    
    def eliminar_asignacion(self, id_asignacion):
        """
        Elimina una asignación específica.
        """
        try:
            cursor = self.conexion.obtener_cursor()
            
            # Eliminamos la asignación específica
            cursor.execute(
                "DELETE FROM asignaciones WHERE id_asignacion = %s",
                (id_asignacion,)
            )
            
            self.conexion.conn.commit()
            deleted = cursor.rowcount > 0
            cursor.close()
            
            if deleted:
                return True
            else:
                print("No se encontró la asignación para eliminar")
                return False
        except Exception as e:
            print(f"Error al eliminar asignación: {e}")
            self.conexion.conn.rollback()
            return False
    
    def cambiar_estado_asignacion(self, id_asignacion, nuevo_estado):
        try:
            cursor = self.conexion.obtener_cursor()
            cursor.execute(
                "UPDATE asignaciones SET estado = %s WHERE id_asignacion = %s",
                (nuevo_estado, id_asignacion)
            )
            self.conexion.conn.commit()
            updated = cursor.rowcount > 0
            cursor.close()
            return updated
        except Exception as e:
            print(f"Error al cambiar estado de asignación: {e}")
            return False