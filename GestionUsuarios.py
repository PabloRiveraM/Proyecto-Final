import psycopg2
from conexion_bd import ConexionBD

class GestionUsuarios:
    def __init__(self, conexion):
        # Guarda la conexión a la base de datos
        self.conexion = conexion
    
    def verificar_credenciales(self, nombre_usuario, contrasena):
        try:
            cursor = self.conexion.obtener_cursor()
            
            # Buscar el usuario en la base de datos
            cursor.execute("SELECT id_usuario, rol FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s", 
                          (nombre_usuario, contrasena))
            
            usuario = cursor.fetchone()
            
            if usuario:
                # Credenciales válidas, devolver información del usuario
                return {
                    'id_usuario': usuario[0],
                    'nombre_usuario': nombre_usuario,
                    'rol': usuario[1],
                    'autenticado': True
                }
            else:
                # Credenciales inválidas
                return {'autenticado': False}
                
        except Exception as error:
            print("Error al verificar credenciales:", error)
            return {'autenticado': False, 'error': str(error)}
            
        finally:
            if cursor:
                cursor.close()