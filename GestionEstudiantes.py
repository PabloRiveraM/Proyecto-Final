from Estudiante import Estudiante
from conexion_bd import ConexionBD

class GestionEstudiantes:
    def __init__(self, conexion):
        self.conexion = conexion

    def listar_estudiantes(self):
        try:
            cursor = self.conexion.obtener_cursor()
            cursor.execute("""
                SELECT id_estudiante, nombre, nombre_contacto, 
                       relacion_contacto, telefono_contacto, 
                       datos_medicos, datos_academicos 
                FROM estudiantes
            """)
            rows = cursor.fetchall()
            estudiantes = []
            for row in rows:
                estudiante = Estudiante(*row)
                estudiantes.append(estudiante)
            cursor.close()
            return estudiantes
        except Exception as e:
            print(f"Error al listar estudiantes: {e}")
            return []



    def buscar_estudiante(self, id_estudiante):
        cursor = self.conexion.obtener_cursor()
        cursor.execute("""
            SELECT id_estudiante, nombre, nombre_contacto, 
                   relacion_contacto, telefono_contacto, 
                   datos_medicos, datos_academicos 
            FROM estudiantes 
            WHERE id_estudiante = %s
        """, (id_estudiante,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Estudiante(*row)
        return None

    def eliminar_estudiante(self, id_estudiante):
        """
        Elimina un estudiante específico sin afectar otros registros.
        Nota: Este método debe ser llamado después de mostrar una modal de confirmación.
        """
        try:
            cursor = self.conexion.obtener_cursor()
            
            # Eliminamos solo el estudiante específico
            cursor.execute(
                "DELETE FROM estudiantes WHERE id_estudiante = %s",
                (id_estudiante,)
            )
            
            self.conexion.conn.commit()
            deleted = cursor.rowcount > 0
            cursor.close()
            
            return deleted
        except Exception as e:
            print(f"Error al eliminar estudiante: {e}")
            self.conexion.conn.rollback()
            return False

    def eliminar_estudiante_con_asignaciones(self, id_estudiante):
        """
        Elimina un estudiante y todas sus asignaciones asociadas.
        Este método se debe llamar después de confirmar con el usuario.
        """
        try:
            cursor = self.conexion.obtener_cursor()
            # Primero eliminamos las asignaciones
            cursor.execute(
                "DELETE FROM asignaciones WHERE id_estudiante = %s",
                (id_estudiante,)
            )
            asignaciones_eliminadas = cursor.rowcount
            
            # Luego eliminamos el estudiante
            cursor.execute(
                "DELETE FROM estudiantes WHERE id_estudiante = %s",
                (id_estudiante,)
            )
            estudiante_eliminado = cursor.rowcount > 0
            
            self.conexion.conn.commit()
            cursor.close()
            
            return {
                "eliminado": estudiante_eliminado,
                "asignaciones_eliminadas": asignaciones_eliminadas
            }
        except Exception as e:
            print(f"Error al eliminar estudiante con asignaciones: {e}")
            self.conexion.conn.rollback()
            return {"error": str(e), "eliminado": False}

    def modificar_estudiante(self, id_estudiante, nombre=None, nombre_contacto=None, 
                            relacion_contacto=None, telefono_contacto=None, 
                            datos_medicos=None, datos_academicos=None):
        cursor = self.conexion.obtener_cursor()
        campos = []
        valores = []
        if nombre:
            campos.append("nombre = %s")
            valores.append(nombre)
        if nombre_contacto:
            campos.append("nombre_contacto = %s")
            valores.append(nombre_contacto)
        if relacion_contacto:
            campos.append("relacion_contacto = %s")
            valores.append(relacion_contacto)
        if telefono_contacto:
            campos.append("telefono_contacto = %s")
            valores.append(telefono_contacto)
        if datos_medicos:
            campos.append("datos_medicos = %s")
            valores.append(datos_medicos)
        if datos_academicos:
            campos.append("datos_academicos = %s")
            valores.append(datos_academicos)
        if not campos:
            cursor.close()
            return False
        valores.append(id_estudiante)
        sql = f"UPDATE estudiantes SET {', '.join(campos)} WHERE id_estudiante = %s"
        cursor.execute(sql, tuple(valores))
        self.conexion.conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        
        
        
        return updated
    
    

    def agregar_estudiante(self, estudiante):
        try:
            cursor = self.conexion.obtener_cursor()
            cursor.execute(
                """INSERT INTO estudiantes 
                (nombre, nombre_contacto, relacion_contacto, telefono_contacto, datos_medicos, datos_academicos) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (estudiante.nombre, estudiante.nombre_contacto, estudiante.relacion_contacto, 
                 estudiante.telefono_contacto, estudiante.datos_medicos, estudiante.datos_academicos)
            )
            self.conexion.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            self.conexion.conn.rollback()  # Hacer rollback explícito
            print(f"Error al agregar estudiante: {e}")
            return False
        
        