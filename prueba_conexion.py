from conexion_bd import ConexionBD

conexion = ConexionBD(
    dbname="postgres",      # O el nombre de tu base de datos
    user="postgres",
    password="Pablo2l3l4l5",
    host="localhost",
    port=5433
)
conexion.conectar()
conexion.cerrar()