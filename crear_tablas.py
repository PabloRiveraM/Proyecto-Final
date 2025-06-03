from conexion_bd import ConexionBD

conexion = ConexionBD(
    dbname="postgres",
    user="postgres",
    password="Pablo2l3l4l5",
    host="localhost",
    port=5433
)
conexion.conectar()

cursor = conexion.obtener_cursor()

# Crear tabla de profesores
cursor.execute("""
CREATE TABLE IF NOT EXISTS profesores (
    id_profesor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    info_contacto VARCHAR(150)
);
""")

# Crear tabla de cursos
cursor.execute("""
CREATE TABLE IF NOT EXISTS cursos (
    id_curso SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    id_profesor INTEGER REFERENCES profesores(id_profesor)
);
""")

# Crear tabla de estudiantes
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nombre_contacto VARCHAR(100),
    relacion_contacto VARCHAR(50),
    telefono_contacto VARCHAR(20),
    datos_medicos TEXT,
    datos_academicos TEXT
);
""")

conexion.conn.commit()
cursor.close()
conexion.cerrar()