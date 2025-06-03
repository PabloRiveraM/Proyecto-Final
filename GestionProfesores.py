from Profesor import Profesor
from conexion_bd import ConexionBD

class GestionProfesores:
    def __init__(self, conexion):
        # Guarda la conexión a la base de datos
        self.conexion = conexion

    def agregar_profesor(self, profesor):
        # Validación básica de los datos del profesor
        if not profesor.nombre or not profesor.info_contacto:
            print("Todos los campos son obligatorios para agregar un profesor.")
            return False
        try:
            cursor = self.conexion.obtener_cursor()
            # Inserta un nuevo profesor en la base de datos
            cursor.execute(
                "INSERT INTO profesores (nombre, info_contacto) VALUES (%s, %s)",
                (profesor.nombre, profesor.info_contacto)
            )
            self.conexion.conn.commit()
            cursor.close()
            print("Profesor agregado correctamente.")
            return True
        except Exception as e:
            print("Error al agregar el profesor:", e)
            return False

    def buscar_profesor(self, id_profesor):
        try:
            cursor = self.conexion.obtener_cursor()
            # Busca un profesor por su ID
            cursor.execute(
                "SELECT id_profesor, nombre, info_contacto FROM profesores WHERE id_profesor = %s",
                (id_profesor,)
            )
            row = cursor.fetchone()
            cursor.close()
            if row:
                return Profesor(*row)
            else:
                print("Profesor no encontrado.")
                return None
        except Exception as e:
            print("Error al buscar el profesor:", e)
            return None

    def eliminar_profesor(self, id_profesor):
        try:
            cursor = self.conexion.obtener_cursor()
            # Elimina un profesor por su ID
            cursor.execute(
                "DELETE FROM profesores WHERE id_profesor = %s",
                (id_profesor,)
            )
            self.conexion.conn.commit()
            deleted = cursor.rowcount > 0
            cursor.close()
            if deleted:
                print("Profesor eliminado correctamente.")
            else:
                print("Profesor no encontrado para eliminar.")
            return deleted
        except Exception as e:
            print("Error al eliminar el profesor:", e)
            return False

    def modificar_profesor(self, id_profesor, nombre=None, info_contacto=None):
        try:
            cursor = self.conexion.obtener_cursor()
            campos = []
            valores = []
            # Solo agrega los campos que se desean modificar
            if nombre:
                campos.append("nombre = %s")
                valores.append(nombre)
            if info_contacto:
                campos.append("info_contacto = %s")
                valores.append(info_contacto)
            if not campos:
                cursor.close()
                print("No se proporcionaron datos para modificar.")
                return False
            valores.append(id_profesor)
            # Actualiza los campos indicados del profesor
            sql = f"UPDATE profesores SET {', '.join(campos)} WHERE id_profesor = %s"
            cursor.execute(sql, tuple(valores))
            self.conexion.conn.commit()
            updated = cursor.rowcount > 0
            cursor.close()
            if updated:
                print("Profesor modificado correctamente.")
            else:
                print("Profesor no encontrado para modificar.")
            return updated
        except Exception as e:
            print("Error al modificar el profesor:", e)
            return False

    def listar_profesores(self):
        try:
            cursor = self.conexion.obtener_cursor()
            # Obtiene todos los profesores de la base de datos
            cursor.execute(
                "SELECT id_profesor, nombre, info_contacto FROM profesores"
            )
            rows = cursor.fetchall()
            cursor.close()
            return [Profesor(*row) for row in rows]
        except Exception as e:
            print("Error al listar los profesores:", e)
            return []