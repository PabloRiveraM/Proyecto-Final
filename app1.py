from flask import Flask, render_template, jsonify, request
from conexion_bd import ConexionBD
from GestionEstudiantes import GestionEstudiantes
from GestionProfesores import GestionProfesores
from GestionCursos import GestionCursos
from Profesor import Profesor
import os
from dotenv import load_dotenv
from GestionAsignaciones import GestionAsignaciones
from flask import session, redirect, url_for
from GestionUsuarios import GestionUsuarios

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar clave secreta para las sesiones - MOVER AQUÍ
app.secret_key = os.urandom(24)

# Configuración de la base de datos usando variables de entorno
conexion = ConexionBD(
    dbname=os.getenv('DB_NAME', 'postgres'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', ''),
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 5432))
)
conexion.conectar()

# Instancias de las clases de gestión
gestion_estudiantes = GestionEstudiantes(conexion)
gestion_profesores = GestionProfesores(conexion)
gestion_cursos = GestionCursos(conexion)
gestion_asignaciones = GestionAsignaciones(conexion)
gestion_usuarios = GestionUsuarios(conexion) 

# Función auxiliar para verificar permisos
def tiene_permiso(roles_permitidos):
    if 'usuario' not in session:
        return False
    return session['usuario']['rol'] in roles_permitidos


@app.route('/login')
def mostrar_login():
    if 'usuario' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
@app.route('/index')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    # Obtener información del usuario desde la sesión
    usuario_id = session['usuario']['id']
    nombre_usuario = session['usuario']['nombre']
    rol_usuario = session['usuario']['rol']
    
    return render_template('index.html', 
                          rol_usuario=rol_usuario, 
                          nombre_usuario=nombre_usuario)

# API para autenticación
@app.route('/api/login', methods=['GET'])
def redirigir_login():
    return redirect(url_for('mostrar_login'))

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    contrasena = data.get('contrasena')
    
    try:
        resultado = gestion_usuarios.verificar_credenciales(nombre_usuario, contrasena)
        
        if resultado['autenticado']:
            session['usuario'] = {
                'id': resultado['id_usuario'],
                'nombre': resultado['nombre_usuario'],
                'rol': resultado['rol']
            }
            return jsonify({
                'exito': True,
                'mensaje': 'Inicio de sesión exitoso',
                'rol': resultado['rol'],
                'nombre': resultado['nombre_usuario']
            })
        else:
            return jsonify({
                'exito': False,
                'mensaje': 'Credenciales inválidas'
            }), 401
            
    except Exception as e:
        return jsonify({
            'exito': False,
            'mensaje': f'Error en el servidor: {str(e)}'
        }), 500

# API para cerrar sesión
@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('usuario', None)
    return jsonify({'exito': True, 'mensaje': 'Sesión cerrada'})



# Rutas para la API de estudiantes
@app.route('/api/estudiantes', methods=['GET'])
def obtener_estudiantes():
    estudiantes = gestion_estudiantes.listar_estudiantes()
    return jsonify([vars(e) for e in estudiantes])

@app.route('/api/estudiantes', methods=['POST'])
def api_agregar_estudiante():
    # Verificar si el usuario tiene permiso para agregar estudiantes
    if not tiene_permiso(['catedratico', 'administrador', 'admin_it']):
        return jsonify({'exito': False, 'mensaje': 'No tiene permisos para realizar esta acción'}), 403
    # Continuar con el código existente para agregar estudiante
    try:
        datos = request.json
        from Estudiante import Estudiante
        estudiante = Estudiante(
            None,  # El ID será asignado por la base de datos
            nombre=datos['nombre'],
            nombre_contacto=datos['nombre_contacto'],
            relacion_contacto=datos['relacion_contacto'],
            telefono_contacto=datos['telefono_contacto'],
            datos_medicos=datos.get('datos_medicos', ''),
            datos_academicos=datos.get('datos_academicos', '')
        )
        gestion_estudiantes.agregar_estudiante(estudiante)
        return jsonify({"mensaje": "Estudiante creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Rutas para la API de profesores
@app.route('/api/profesores', methods=['GET'])
def obtener_profesores():
    profesores = gestion_profesores.listar_profesores()
    return jsonify([vars(p) for p in profesores])

@app.route('/api/profesores', methods=['POST'])
def api_agregar_profesor():
    # Verificar si el usuario tiene permiso para agregar profesores
    if not tiene_permiso(['administrador', 'admin_it']):
        return jsonify({'exito': False, 'mensaje': 'No tiene permisos para realizar esta acción'}), 403
    
    # Continuar con el código existente para agregar profesor
    try:
        datos = request.json
        # Crear un objeto Profesor primero
        from Profesor import Profesor
        profesor = Profesor(
            None,  # El ID será asignado por la base de datos
            nombre=datos['nombre'],
            info_contacto=datos['info_contacto']
        )
        # Usar el método agregar_profesor que debería existir
        gestion_profesores.agregar_profesor(profesor)
        return jsonify({"mensaje": "Profesor creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rutas para la API de cursos
@app.route('/api/cursos', methods=['GET'])
def obtener_cursos():
    cursos = gestion_cursos.listar_cursos()
    return jsonify([vars(c) for c in cursos])

@app.route('/api/cursos', methods=['POST'])
def crear_curso():
    try:
        datos = request.json
        # Crear un objeto Curso primero
        from Curso import Curso
        curso = Curso(
            None,  # El ID será asignado por la base de datos
            nombre=datos['nombre'],
            descripcion=datos.get('descripcion', ''),
            id_profesor=datos['id_profesor']
        )
        # Usar el método agregar_curso que debería existir
        gestion_cursos.agregar_curso(curso)
        return jsonify({"mensaje": "Curso creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rutas para obtener un estudiante específico
@app.route('/api/estudiantes/<int:id_estudiante>', methods=['GET'])
def buscar_estudiante(id_estudiante):
    try:
        estudiante = gestion_estudiantes.buscar_estudiante(id_estudiante)
        return jsonify(vars(estudiante))
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Rutas para actualizar un estudiante
@app.route('/api/estudiantes/<int:id_estudiante>', methods=['PUT'])
def actualizar_estudiante(id_estudiante):
    try:
        datos = request.json
        estudiante = gestion_estudiantes.modificar_estudiante(
            id_estudiante=id_estudiante,
            nombre=datos['nombre'],
            nombre_contacto=datos['nombre_contacto'],
            relacion_contacto=datos['relacion_contacto'],
            telefono_contacto=datos['telefono_contacto'],
            datos_medicos=datos.get('datos_medicos', ''),
            datos_academicos=datos.get('datos_academicos', '')
        )
        return jsonify({"mensaje": "Estudiante actualizado exitosamente", "id": id_estudiante})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Implementar rutas similares para profesores y cursos
@app.route('/api/estudiantes/<int:id_estudiante>', methods=['DELETE'])
def eliminar_estudiante(id_estudiante):
    try:
        gestion_estudiantes.eliminar_estudiante(id_estudiante)
        return jsonify({"mensaje": "Estudiante eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rutas para eliminar profesores
@app.route('/api/profesores/<int:id_profesor>', methods=['DELETE'])
def eliminar_profesor(id_profesor):
    try:
        gestion_profesores.eliminar_profesor(id_profesor)
        return jsonify({"mensaje": "Profesor eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rutas para eliminar cursos
@app.route('/api/cursos/<int:id_curso>', methods=['DELETE'])
def eliminar_curso(id_curso):
    try:
        gestion_cursos.eliminar_curso(id_curso)
        return jsonify({"mensaje": "Curso eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para obtener un profesor específico
@app.route('/api/profesores/<int:id_profesor>', methods=['GET'])
def obtener_profesor(id_profesor):
    try:
        profesor = gestion_profesores.buscar_profesor(id_profesor)
        return jsonify(vars(profesor))
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Ruta para obtener un curso específico
@app.route('/api/cursos/<int:id_curso>', methods=['GET'])
def obtener_curso(id_curso):
    try:
        curso = gestion_cursos.buscar_curso(id_curso)
        return jsonify(vars(curso))
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Inicializar la gestión de asignaciones
gestion_asignaciones = GestionAsignaciones(conexion)

@app.route('/api/asignaciones', methods=['GET'])
def obtener_asignaciones():
    asignaciones = gestion_asignaciones.listar_asignaciones()
    return jsonify(asignaciones)

@app.route('/api/asignaciones', methods=['POST'])
def crear_asignacion():
    try:
        datos = request.json
        id_estudiante = datos.get('id_estudiante')
        id_curso = datos.get('id_curso')
        
        if not id_estudiante or not id_curso:
            return jsonify({"error": "Se requiere ID de estudiante y curso"}), 400
            
        resultado = gestion_asignaciones.asignar_curso(id_estudiante, id_curso)
        if resultado:
            return jsonify({"mensaje": "Curso asignado correctamente"}), 201
        else:
            return jsonify({"error": "Error al asignar curso"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/asignaciones/<int:id_asignacion>', methods=['DELETE'])
def eliminar_asignacion(id_asignacion):
    # Verificar si el usuario tiene permiso para eliminar asignaciones
    if not tiene_permiso(['administrador', 'admin_it']):
        return jsonify({'exito': False, 'mensaje': 'No tiene permisos para realizar esta acción'}), 403
    
    try:
        resultado = gestion_asignaciones.eliminar_asignacion(id_asignacion)
        if resultado:
            return jsonify({"mensaje": "Asignación eliminada correctamente"})
        else:
            return jsonify({"error": "Asignación no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/asignaciones/<int:id_asignacion>/estado', methods=['PUT'])
def actualizar_estado_asignacion(id_asignacion):
    try:
        datos = request.json
        nuevo_estado = datos.get('estado')
        
        if not nuevo_estado:
            return jsonify({"error": "Se requiere el nuevo estado"}), 400
            
        resultado = gestion_asignaciones.cambiar_estado_asignacion(id_asignacion, nuevo_estado)
        if resultado:
            return jsonify({"mensaje": "Estado actualizado correctamente"})
        else:
            return jsonify({"error": "Asignación no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API para obtener información del usuario actual
@app.route('/api/usuario-actual')
def api_usuario_actual():
    if 'usuario' in session:
        return jsonify({
            'autenticado': True,
            'id': session['usuario']['id'],
            'nombre': session['usuario']['nombre'],
            'rol': session['usuario']['rol']
        })
    else:
        return jsonify({'autenticado': False})
    # ... existing code ...

@app.route('/logout')
def logout():
    # Eliminar datos de sesión si existen
    session.pop('usuario', None)
    # Redireccionar a la página de login
    return redirect(url_for('mostrar_login'))

if __name__ == '__main__':
    app.run(debug=True)