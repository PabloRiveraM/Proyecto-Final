from Curso import Curso
from conexion_bd import ConexionBD

class GestionCursos:
    def __init__(self, conexion):
        # Guarda la conexión a la base de datos
        self.conexion = conexion

    def agregar_curso(self, curso):
        # Validación básica de los datos del curso
        if not curso.nombre or not curso.descripcion or not curso.id_profesor:
            print("Todos los campos son obligatorios para agregar un curso.")
            return False
        try:
            cursor = self.conexion.obtener_cursor()
            # Inserta un nuevo curso en la base de datos
            cursor.execute(
                "INSERT INTO cursos (nombre, descripcion, id_profesor) VALUES (%s, %s, %s)",
                (curso.nombre, curso.descripcion, curso.id_profesor)
            )
            self.conexion.conn.commit()
            cursor.close()
            print("Curso agregado correctamente.")
            return True
        except Exception as e:
            print("Error al agregar el curso:", e)
            return False

    def buscar_curso(self, id_curso):
        try:
            cursor = self.conexion.obtener_cursor()
            # Busca un curso por su ID
            cursor.execute(
                "SELECT id_curso, nombre, descripcion, id_profesor FROM cursos WHERE id_curso = %s",
                (id_curso,)
            )
            row = cursor.fetchone()
            cursor.close()
            if row:
                return Curso(*row)
            else:
                print("Curso no encontrado.")
                return None
        except Exception as e:
            print("Error al buscar el curso:", e)
            return None

    def eliminar_curso(self, id_curso):
        try:
            cursor = self.conexion.obtener_cursor()
            # Elimina un curso por su ID
            cursor.execute(
                "DELETE FROM cursos WHERE id_curso = %s",
                (id_curso,)
            )
            self.conexion.conn.commit()
            deleted = cursor.rowcount > 0
            cursor.close()
            if deleted:
                print("Curso eliminado correctamente.")
            else:
                print("Curso no encontrado para eliminar.")
            return deleted
        except Exception as e:
            print("Error al eliminar el curso:", e)
            return False

    def modificar_curso(self, id_curso, nombre=None, descripcion=None, id_profesor=None):
        try:
            cursor = self.conexion.obtener_cursor()
            campos = []
            valores = []
            # Solo agrega los campos que se desean modificar
            if nombre:
                campos.append("nombre = %s")
                valores.append(nombre)
            if descripcion:
                campos.append("descripcion = %s")
                valores.append(descripcion)
            if id_profesor:
                campos.append("id_profesor = %s")
                valores.append(id_profesor)
            if not campos:
                cursor.close()
                print("No se proporcionaron datos para modificar.")
                return False
            valores.append(id_curso)
            sql = f"UPDATE cursos SET {', '.join(campos)} WHERE id_curso = %s"
            cursor.execute(sql, tuple(valores))
            self.conexion.conn.commit()
            updated = cursor.rowcount > 0
            cursor.close()
            if updated:
                print("Curso modificado correctamente.")
            else:
                print("Curso no encontrado para modificar.")
            return updated
        except Exception as e:
            print("Error al modificar el curso:", e)
            return False

    def listar_cursos(self):
        try:
            cursor = self.conexion.obtener_cursor()
            # Obtiene todos los cursos de la base de datos
            cursor.execute(
                "SELECT id_curso, nombre, descripcion, id_profesor FROM cursos"
            )
            rows = cursor.fetchall()
            cursor.close()
            return [Curso(*row) for row in rows]
        except Exception as e:
            print("Error al listar los cursos:", e)
            return []