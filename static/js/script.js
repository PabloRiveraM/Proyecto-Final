// Funciones para manejar la navegación
function mostrarSeccion(seccionId) {
    document.querySelectorAll('.seccion-contenido').forEach(seccion => {
        seccion.classList.remove('activa');
    });
    document.getElementById(seccionId).classList.add('activa');
}

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    mostrarSeccion('estudiantes');
    cargarEstudiantes();
    cargarProfesores();
    cargarCursos();
    cargarAsignaciones();
    document.getElementById('form-estudiante').addEventListener('submit', agregarEstudiante);
    document.getElementById('form-profesor').addEventListener('submit', agregarProfesor);
    document.getElementById('form-curso').addEventListener('submit', agregarCurso);
    document.getElementById('form-asignacion').addEventListener('submit', asignarCurso);
    cargarProfesoresEnSelector();
    cargarEstudiantesEnSelector();
    cargarCursosEnSelector();
});

// Cargar profesores en el selector de cursos
async function cargarProfesoresEnSelector() {
    try {
        const response = await fetch('/api/profesores');
        const profesores = await response.json();
        const select = document.getElementById('profesor-curso');
        select.innerHTML = '';
        profesores.forEach(profesor => {
            const option = document.createElement('option');
            option.value = profesor.id_profesor;
            option.textContent = profesor.nombre;
            select.appendChild(option);
        });
    } catch (error) {
        mostrarMensaje('Error al cargar profesores', 'error');
    }
}

// Cargar estudiantes
async function cargarEstudiantes() {
    try {
        const response = await fetch('/api/estudiantes');
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        const estudiantes = await response.json();
        const tbody = document.querySelector('#tabla-estudiantes tbody');
        tbody.innerHTML = '';
        if (estudiantes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">No hay estudiantes registrados</td></tr>';
            return;
        }
        
        const tienePermisos = tienePermisosEdicion();
        
        estudiantes.forEach(estudiante => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${estudiante.id_estudiante || ''}</td>
                <td>${estudiante.nombre || ''}</td>
                <td>${estudiante.nombre_contacto || ''}</td>
                <td>${estudiante.relacion_contacto || ''}</td>
                <td>${estudiante.telefono_contacto || ''}</td>
                <td>
                    ${tienePermisos ? `
                        <button class="btn-editar" onclick="editarEstudiante(${estudiante.id_estudiante})">Editar</button>
                        <button class="btn-eliminar" onclick="eliminarEstudiante(${estudiante.id_estudiante})">Eliminar</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error detallado:', error);
        mostrarMensaje(`Error al cargar estudiantes: ${error.message}`, 'error');
    }
}

// Cargar profesores
async function cargarProfesores() {
    try {
        const response = await fetch('/api/profesores');
        const profesores = await response.json();
        const tbody = document.querySelector('#tabla-profesores tbody');
        tbody.innerHTML = '';
        
        const tienePermisos = tienePermisosEdicion();
        
        profesores.forEach(profesor => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${profesor.id_profesor}</td>
                <td>${profesor.nombre}</td>
                <td>${profesor.info_contacto}</td>
                <td>
                    ${tienePermisos ? `
                        <button onclick="editarProfesor(${profesor.id_profesor})" class="btn-editar">Editar</button>
                        <button onclick="eliminarProfesor(${profesor.id_profesor})" class="btn-eliminar">Eliminar</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        mostrarMensaje('Error al cargar profesores', 'error');
    }
}

// Cargar cursos
async function cargarCursos() {
    try {
        const response = await fetch('/api/cursos');
        const cursos = await response.json();
        const tbody = document.querySelector('#tabla-cursos tbody');
        tbody.innerHTML = '';
        
        const tienePermisos = tienePermisosEdicion();
        
        cursos.forEach(curso => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${curso.id_curso}</td>
                <td>${curso.nombre}</td>
                <td>${curso.descripcion}</td>
                <td>${curso.id_profesor}</td>
                <td>
                    ${tienePermisos ? `
                        <button onclick="editarCurso(${curso.id_curso})" class="btn-editar">Editar</button>
                        <button onclick="eliminarCurso(${curso.id_curso})" class="btn-eliminar">Eliminar</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        mostrarMensaje('Error al cargar cursos', 'error');
    }
}

// Validar formularios
function validarFormulario(formData, tipo) {
    const errores = [];
    switch (tipo) {
        case 'estudiante':
            if (!formData.nombre || formData.nombre.trim() === '') {
                errores.push('El nombre del estudiante es obligatorio');
            }
            if (!formData.nombre_contacto || formData.nombre_contacto.trim() === '') {
                errores.push('El nombre del contacto es obligatorio');
            }
            if (!formData.telefono_contacto || formData.telefono_contacto.trim() === '') {
                errores.push('El teléfono del contacto es obligatorio');
            }
            break;
        case 'profesor':
            if (!formData.nombre || formData.nombre.trim() === '') {
                errores.push('El nombre del profesor es obligatorio');
            }
            if (!formData.info_contacto || formData.info_contacto.trim() === '') {
                errores.push('La información de contacto es obligatoria');
            }
            break;
        case 'curso':
            if (!formData.nombre || formData.nombre.trim() === '') {
                errores.push('El nombre del curso es obligatorio');
            }
            if (!formData.id_profesor) {
                errores.push('Debe seleccionar un profesor para el curso');
            }
            break;
    }
    return errores;
}

// Agregar o actualizar estudiante
async function agregarEstudiante(event) {
    event.preventDefault();
    const form = event.target;
    const isEditing = form.getAttribute('data-editing') === 'true';
    const id = form.getAttribute('data-id');
    const formData = {
        nombre: document.getElementById('nombre').value,
        nombre_contacto: document.getElementById('nombre_contacto').value,
        relacion_contacto: document.getElementById('relacion_contacto').value,
        telefono_contacto: document.getElementById('telefono_contacto').value,
        datos_medicos: document.getElementById('medicos').value,
        datos_academicos: document.getElementById('academicos').value
    };
    const errores = validarFormulario(formData, 'estudiante');
    if (errores.length > 0) {
        mostrarMensaje(errores.join('. '), 'error');
        return;
    }
    try {
        let url = '/api/estudiantes';
        let method = 'POST';
        if (isEditing) {
            url = `/api/estudiantes/${id}`;
            method = 'PUT';
        }
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        const mensaje = isEditing ? 'Estudiante actualizado correctamente' : 'Estudiante agregado correctamente';
        mostrarMensaje(mensaje, 'success');
        form.reset();
        form.removeAttribute('data-editing');
        form.removeAttribute('data-id');
        const botonSubmit = form.querySelector('button[type="submit"]');
        botonSubmit.textContent = 'Agregar Estudiante';
        cargarEstudiantes();
    } catch (error) {
        mostrarMensaje('Error al procesar la solicitud: ' + error.message, 'error');
    }
}

// Agregar o actualizar profesor
async function agregarProfesor(event) {
    event.preventDefault();
    const form = event.target;
    const isEditing = form.getAttribute('data-editing') === 'true';
    const id = form.getAttribute('data-id');
    const formData = {
        nombre: document.getElementById('nombre-profesor').value,
        info_contacto: document.getElementById('contacto-profesor').value
    };
    const errores = validarFormulario(formData, 'profesor');
    if (errores.length > 0) {
        mostrarMensaje(errores.join('. '), 'error');
        return;
    }
    try {
        let url = '/api/profesores';
        let method = 'POST';
        if (isEditing) {
            url = `/api/profesores/${id}`;
            method = 'PUT';
        }
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        const mensaje = isEditing ? 'Profesor actualizado correctamente' : 'Profesor agregado correctamente';
        mostrarMensaje(mensaje, 'success');
        form.reset();
        form.removeAttribute('data-editing');
        form.removeAttribute('data-id');
        const botonSubmit = form.querySelector('button[type="submit"]');
        botonSubmit.textContent = 'Agregar Profesor';
        cargarProfesores();
        cargarProfesoresEnSelector();
    } catch (error) {
        mostrarMensaje('Error al procesar la solicitud: ' + error.message, 'error');
    }
}

// Agregar o actualizar curso
async function agregarCurso(event) {
    event.preventDefault();
    const form = event.target;
    const isEditing = form.getAttribute('data-editing') === 'true';
    const id = form.getAttribute('data-id');
    const formData = {
        nombre: document.getElementById('nombre-curso').value,
        descripcion: document.getElementById('descripcion').value,
        id_profesor: document.getElementById('profesor-curso').value
    };
    const errores = validarFormulario(formData, 'curso');
    if (errores.length > 0) {
        mostrarMensaje(errores.join('. '), 'error');
        return;
    }
    try {
        let url = '/api/cursos';
        let method = 'POST';
        if (isEditing) {
            url = `/api/cursos/${id}`;
            method = 'PUT';
        }
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        const mensaje = isEditing ? 'Curso actualizado correctamente' : 'Curso agregado correctamente';
        mostrarMensaje(mensaje, 'success');
        form.reset();
        form.removeAttribute('data-editing');
        form.removeAttribute('data-id');
        const botonSubmit = form.querySelector('button[type="submit"]');
        botonSubmit.textContent = 'Agregar Curso';
        cargarCursos();
    } catch (error) {
        mostrarMensaje('Error al procesar la solicitud: ' + error.message, 'error');
    }
}

// Editar estudiante
function editarEstudiante(id) {
    fetch(`/api/estudiantes/${id}`)
        .then(response => {
            if (!response.ok) throw new Error('Error al obtener datos del estudiante');
            return response.json();
        })
        .then(estudiante => {
            document.getElementById('nombre').value = estudiante.nombre || '';
            document.getElementById('nombre_contacto').value = estudiante.nombre_contacto || '';
            document.getElementById('relacion_contacto').value = estudiante.relacion_contacto || '';
            document.getElementById('telefono_contacto').value = estudiante.telefono_contacto || '';
            document.getElementById('medicos').value = estudiante.datos_medicos || '';
            document.getElementById('academicos').value = estudiante.datos_academicos || '';
            const form = document.getElementById('form-estudiante');
            form.setAttribute('data-editing', 'true');
            form.setAttribute('data-id', id);
            const botonSubmit = form.querySelector('button[type="submit"]');
            botonSubmit.textContent = `Actualizar Estudiante: ${estudiante.nombre}`;
            form.classList.add('modo-edicion');
            mostrarMensaje(`Editando estudiante: ${estudiante.nombre}`, 'info');
            form.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            mostrarMensaje('Error al cargar los datos del estudiante', 'error');
        });
}

// Editar profesor
async function editarProfesor(id) {
    try {
        const response = await fetch(`/api/profesores/${id}`);
        if (!response.ok) throw new Error('Error al obtener datos del profesor');
        const profesor = await response.json();
        document.getElementById('nombre-profesor').value = profesor.nombre || '';
        document.getElementById('contacto-profesor').value = profesor.info_contacto || '';
        const form = document.getElementById('form-profesor');
        form.setAttribute('data-editing', 'true');
        form.setAttribute('data-id', id);
        const botonSubmit = form.querySelector('button[type="submit"]');
        botonSubmit.textContent = `Actualizar Profesor: ${profesor.nombre}`;
        form.classList.add('modo-edicion');
        mostrarMensaje(`Editando profesor: ${profesor.nombre}`, 'info');
        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        mostrarMensaje('Error al cargar los datos del profesor', 'error');
    }
}

// Editar curso
async function editarCurso(id) {
    try {
        const response = await fetch(`/api/cursos/${id}`);
        if (!response.ok) throw new Error('Error al obtener datos del curso');
        const curso = await response.json();
        document.getElementById('nombre-curso').value = curso.nombre || '';
        document.getElementById('descripcion').value = curso.descripcion || '';
        document.getElementById('profesor-curso').value = curso.id_profesor || '';
        const form = document.getElementById('form-curso');
        form.setAttribute('data-editing', 'true');
        form.setAttribute('data-id', id);
        const botonSubmit = form.querySelector('button[type="submit"]');
        botonSubmit.textContent = `Actualizar Curso: ${curso.nombre}`;
        form.classList.add('modo-edicion');
        mostrarMensaje(`Editando curso: ${curso.nombre}`, 'info');
        form.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        mostrarMensaje('Error al cargar los datos del curso', 'error');
    }
}

// Función para crear modal de confirmación
function crearModalConfirmacion(mensaje, onConfirm) {
    const modalHTML = `
        <div class="modal-confirmacion" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        ">
            <div style="
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 90%;
            ">
                <h3 style="margin-top: 0;">Confirmar Acción</h3>
                <p>${mensaje}</p>
                <div style="
                    display: flex;
                    justify-content: flex-end;
                    gap: 10px;
                    margin-top: 20px;
                ">
                    <button class="btn-cancelar" style="
                        padding: 8px 16px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        background-color: #6c757d;
                        color: white;
                    ">Cancelar</button>
                    <button class="btn-confirmar" style="
                        padding: 8px 16px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        background-color: #dc3545;
                        color: white;
                    ">Confirmar</button>
                </div>
            </div>
        </div>
    `;

    const modalElement = document.createElement('div');
    modalElement.innerHTML = modalHTML;
    document.body.appendChild(modalElement.firstElementChild);

    const modal = document.querySelector('.modal-confirmacion');
    const btnConfirmar = modal.querySelector('.btn-confirmar');
    const btnCancelar = modal.querySelector('.btn-cancelar');

    btnConfirmar.addEventListener('click', () => {
        onConfirm();
        modal.remove();
    });

    btnCancelar.addEventListener('click', () => {
        modal.remove();
    });
}

// Modificar las funciones de eliminar para usar el modal
async function eliminarEstudiante(id) {
    crearModalConfirmacion('¿Estás seguro de que deseas eliminar este estudiante?', async () => {
        try {
            const response = await fetch(`/api/estudiantes/${id}`, { method: 'DELETE' });
            if (response.ok) {
                mostrarMensaje('Estudiante eliminado correctamente', 'success');
                cargarEstudiantes();
            } else {
                mostrarMensaje('Error al eliminar estudiante', 'error');
            }
        } catch (error) {
            mostrarMensaje('Error al procesar la solicitud', 'error');
        }
    });
}

async function eliminarProfesor(id) {
    crearModalConfirmacion('¿Estás seguro de que deseas eliminar este profesor?', async () => {
        try {
            const response = await fetch(`/api/profesores/${id}`, { method: 'DELETE' });
            if (response.ok) {
                mostrarMensaje('Profesor eliminado correctamente', 'success');
                cargarProfesores();
            } else {
                mostrarMensaje('Error al eliminar profesor', 'error');
            }
        } catch (error) {
            mostrarMensaje('Error al procesar la solicitud', 'error');
        }
    });
}

async function eliminarCurso(id) {
    crearModalConfirmacion('¿Estás seguro de que deseas eliminar este curso?', async () => {
        try {
            const response = await fetch(`/api/cursos/${id}`, { method: 'DELETE' });
            if (response.ok) {
                mostrarMensaje('Curso eliminado correctamente', 'success');
                cargarCursos();
            } else {
                mostrarMensaje('Error al eliminar curso', 'error');
            }
        } catch (error) {
            mostrarMensaje('Error al procesar la solicitud', 'error');
        }
    });
}

// Mostrar mensajes
function mostrarMensaje(mensaje, tipo) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo}`;
    alertDiv.style.padding = '10px';
    alertDiv.style.margin = '10px 0';
    alertDiv.style.borderRadius = '5px';
    switch(tipo) {
        case 'success':
            alertDiv.style.backgroundColor = '#d4edda';
            alertDiv.style.color = '#155724';
            break;
        case 'error':
            alertDiv.style.backgroundColor = '#f8d7da';
            alertDiv.style.color = '#721c24';
            break;
        case 'info':
            alertDiv.style.backgroundColor = '#cce5ff';
            alertDiv.style.color = '#004085';
            break;
    }
    alertDiv.textContent = mensaje;
    const container = document.querySelector('main');
    container.insertBefore(alertDiv, container.firstChild);
    setTimeout(() => alertDiv.remove(), 3000);
}

// Estilos dinámicos para modo edición
const style = document.createElement('style');
style.textContent = `
    .modo-edicion {
        background-color: #f8f9fa;
        padding: 20px;
        border: 2px solid #007bff;
        border-radius: 5px;
        transition: all 0.3s ease;
        margin: 10px 0;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .modo-edicion button[type="submit"] {
        background-color: #28a745;
        color: white;
    }
`;
document.head.appendChild(style);

// Cargar estudiantes en el selector de asignaciones
async function cargarEstudiantesEnSelector() {
    try {
        const response = await fetch('/api/estudiantes');
        const estudiantes = await response.json();
        const select = document.getElementById('estudiante-asignacion');
        select.innerHTML = '';
        estudiantes.forEach(estudiante => {
            const option = document.createElement('option');
            option.value = estudiante.id_estudiante;
            option.textContent = estudiante.nombre;
            select.appendChild(option);
        });
    } catch (error) {
        mostrarMensaje('Error al cargar estudiantes', 'error');
    }
}

// Cargar cursos en el selector de asignaciones
async function cargarCursosEnSelector() {
    try {
        const response = await fetch('/api/cursos');
        const cursos = await response.json();
        const select = document.getElementById('curso-asignacion');
        select.innerHTML = '';
        cursos.forEach(curso => {
            const option = document.createElement('option');
            option.value = curso.id_curso;
            option.textContent = curso.nombre;
            select.appendChild(option);
        });
    } catch (error) {
        mostrarMensaje('Error al cargar cursos', 'error');
    }
}

// Cargar asignaciones
async function cargarAsignaciones() {
    try {
        const response = await fetch('/api/asignaciones');
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        const asignaciones = await response.json();
        const tbody = document.querySelector('#tabla-asignaciones tbody');
        tbody.innerHTML = '';
        
        if (asignaciones.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No hay asignaciones registradas</td></tr>';
            return;
        }
        
        const tienePermisos = tienePermisosEdicion();
        
        asignaciones.forEach(asignacion => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${asignacion.id_asignacion || ''}</td>
                <td>${asignacion.nombre_estudiante || ''}</td>
                <td>${asignacion.nombre_curso || ''}</td>
                <td>${asignacion.nombre_profesor || ''}</td>
                <td>${asignacion.fecha_asignacion || ''}</td>
                <td>${asignacion.estado || ''}</td>
                <td>
                    ${tienePermisos ? `
                        <button class="btn-editar" onclick="cambiarEstadoAsignacion(${asignacion.id_asignacion})">Cambiar Estado</button>
                        <button class="btn-eliminar" onclick="eliminarAsignacion(${asignacion.id_asignacion})">Eliminar</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error detallado:', error);
        mostrarMensaje(`Error al cargar asignaciones: ${error.message}`, 'error');
    }
}


// Asignar curso a estudiante
async function asignarCurso(event) {
    event.preventDefault();
    const id_estudiante = document.getElementById('estudiante-asignacion').value;
    const id_curso = document.getElementById('curso-asignacion').value;
    
    if (!id_estudiante || !id_curso) {
        mostrarMensaje('Debe seleccionar un estudiante y un curso', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/asignaciones', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id_estudiante, id_curso })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        
        mostrarMensaje('Curso asignado correctamente', 'success');
        cargarAsignaciones();
    } catch (error) {
        mostrarMensaje(`Error al asignar curso: ${error.message}`, 'error');
    }
}

// Eliminar asignación
async function eliminarAsignacion(id_asignacion) {
    if (!confirm('¿Está seguro de eliminar esta asignación?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/asignaciones/${id_asignacion}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        
        mostrarMensaje('Asignación eliminada correctamente', 'success');
        cargarAsignaciones();
    } catch (error) {
        mostrarMensaje(`Error al eliminar asignación: ${error.message}`, 'error');
    }
}

// Cambiar estado de asignación
async function cambiarEstadoAsignacion(id_asignacion) {
    const nuevoEstado = prompt('Ingrese el nuevo estado (Activo, Completado, Suspendido):');
    if (!nuevoEstado) {
        return;
    }
    
    try {
        const response = await fetch(`/api/asignaciones/${id_asignacion}/estado`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ estado: nuevoEstado })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        
        mostrarMensaje('Estado actualizado correctamente', 'success');
        cargarAsignaciones();
    } catch (error) {
        mostrarMensaje(`Error al actualizar estado: ${error.message}`, 'error');
    }
}

// Variables globales
let rolUsuario = '';

// Función para obtener el rol del usuario desde la sesión
function obtenerRolUsuario() {
    fetch('/api/usuario-actual')
        .then(response => response.json())
        .then(data => {
            if (data.autenticado) {
                rolUsuario = data.rol;
                aplicarPermisosSegunRol();
            } else {
                // Si no hay sesión, redirigir al login
                window.location.href = '/';
            }
        })
        .catch(error => {
            console.error('Error al obtener información del usuario:', error);
        });
}

// Función para aplicar permisos según el rol
// Función para aplicar permisos según el rol
function aplicarPermisosSegunRol() {
    console.log("Rol del usuario:", rolUsuario);
    
    // Obtener todos los botones y campos de entrada
    const botonesAgregar = document.querySelectorAll('.btn-agregar');
    const botonesEditar = document.querySelectorAll('.btn-editar');
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    const botonesCambiarEstado = document.querySelectorAll('.btn-cambiar-estado');
    const inputsFormularios = document.querySelectorAll('input, select, textarea');
    
    // Configurar según el rol
    if (rolUsuario === 'estudiante') {
        // Deshabilitar todos los botones de acción
        botonesAgregar.forEach(btn => btn.disabled = true);
        botonesEditar.forEach(btn => btn.disabled = true);
        botonesEliminar.forEach(btn => btn.disabled = true);
        botonesCambiarEstado.forEach(btn => btn.disabled = true);
        
        // Deshabilitar específicamente los botones en la sección de asignaciones
        document.querySelectorAll('#asignaciones-actuales .btn').forEach(btn => {
            btn.disabled = true;
            btn.classList.add('disabled');
        });
        
        // Deshabilitar el botón "Asignar Curso"
        const btnAsignarCurso = document.querySelector('#btn-asignar-curso');
        if (btnAsignarCurso) {
            btnAsignarCurso.disabled = true;
            btnAsignarCurso.classList.add('disabled');
        }
        
        // Deshabilitar todos los campos de entrada en formularios
        inputsFormularios.forEach(input => input.disabled = true);
        
        // Opcional: Añadir clase CSS para mostrar visualmente que están deshabilitados
        botonesAgregar.forEach(btn => btn.classList.add('disabled'));
        botonesEditar.forEach(btn => btn.classList.add('disabled'));
        botonesEliminar.forEach(btn => btn.classList.add('disabled'));
        botonesCambiarEstado.forEach(btn => btn.classList.add('disabled'));
    } else if (rolUsuario === 'catedratico') {
        // Habilitar solo lo que corresponde a catedráticos
        // Puede agregar y editar estudiantes
        document.querySelectorAll('#estudiantes .btn-agregar, #tabla-estudiantes .btn-editar')
            .forEach(btn => {
                btn.disabled = false;
                btn.classList.remove('disabled');
            });
    } else if (rolUsuario === 'administrador') {
        // Habilitar lo que corresponde a administradores
        document.querySelectorAll('#estudiantes .btn-agregar, #profesores .btn-agregar, #asignaciones .btn-agregar')
            .forEach(btn => {
                btn.disabled = false;
                btn.classList.remove('disabled');
            });
        
        document.querySelectorAll('#tabla-estudiantes .btn-editar, #tabla-estudiantes .btn-eliminar, #tabla-profesores .btn-editar, #tabla-profesores .btn-eliminar, #tabla-asignaciones .btn-editar, #tabla-asignaciones .btn-eliminar')
            .forEach(btn => {
                btn.disabled = false;
                btn.classList.remove('disabled');
            });
    } else if (rolUsuario === 'admin_it') {
        // Acceso total para admin_it
        botonesAgregar.forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('disabled');
        });
        botonesEditar.forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('disabled');
        });
        botonesEliminar.forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('disabled');
        });
        inputsFormularios.forEach(input => input.disabled = false);
    }
    
    // Mostrar el rol en la interfaz
    const headerInfo = document.createElement('div');
    headerInfo.classList.add('usuario-info');
    headerInfo.textContent = `Usuario: ${rolUsuario}`;
    document.querySelector('header').appendChild(headerInfo);
}

// Agregar función para cerrar sesión
function cerrarSesion() {
    fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.exito) {
            window.location.href = '/';
        }
    })
    .catch(error => {
        console.error('Error al cerrar sesión:', error);
    });
}

// Modificar el evento DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // ... existing code ...
    
    // Obtener el rol del usuario y aplicar permisos
    obtenerRolUsuario();
    
    // Agregar botón de cerrar sesión al header
    const header = document.querySelector('header');
    const btnLogout = document.createElement('button');
    btnLogout.textContent = 'Cerrar Sesión';
    btnLogout.classList.add('btn-logout');
    btnLogout.addEventListener('click', cerrarSesion);
    header.appendChild(btnLogout);
});


// Función para verificar si el usuario tiene permisos
function tienePermisosEdicion() {
    const rolUsuario = localStorage.getItem('rol_usuario');
    return rolUsuario && rolUsuario !== 'estudiante';
}

// Modificar la función cargarEstudiantes
async function cargarEstudiantes() {
    try {
        const response = await fetch('/api/estudiantes');
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error HTTP: ${response.status}`);
        }
        const estudiantes = await response.json();
        const tbody = document.querySelector('#tabla-estudiantes tbody');
        tbody.innerHTML = '';
        if (estudiantes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">No hay estudiantes registrados</td></tr>';
            return;
        }
        
        const tienePermisos = tienePermisosEdicion();
        
        estudiantes.forEach(estudiante => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${estudiante.id_estudiante || ''}</td>
                <td>${estudiante.nombre || ''}</td>
                <td>${estudiante.nombre_contacto || ''}</td>
                <td>${estudiante.relacion_contacto || ''}</td>
                <td>${estudiante.telefono_contacto || ''}</td>
                <td>
                    ${tienePermisos ? `
                        <button class="btn-editar" onclick="editarEstudiante(${estudiante.id_estudiante})">Editar</button>
                        <button class="btn-eliminar" onclick="eliminarEstudiante(${estudiante.id_estudiante})">Eliminar</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error detallado:', error);
        mostrarMensaje(`Error al cargar estudiantes: ${error.message}`, 'error');
    }
}

// Modificar la función cargarProfesores
async function cargarProfesores() {
    try {
        const response = await fetch('/api/profesores');
        const profesores = await response.json();
        const tbody = document.querySelector('#tabla-profesores tbody');
        tbody.innerHTML = '';
        
        const tienePermisos = tienePermisosEdicion();
        
        profesores.forEach(profesor => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${profesor.id_profesor}</td>
                <td>${profesor.nombre}</td>
                <td>${profesor.info_contacto}</td>
                <td>
                    ${tienePermisos ? `
                        <button onclick="editarProfesor(${profesor.id_profesor})" class="btn-editar">Editar</button>
                        <button onclick="eliminarProfesor(${profesor.id_profesor})" class="btn-eliminar">Eliminar</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        mostrarMensaje('Error al cargar profesores', 'error');
    }
}

// Modificar la función cargarCursos
async function cargarCursos() {
    try {
        const response = await fetch('/api/cursos');
        const cursos = await response.json();
        const tbody = document.querySelector('#tabla-cursos tbody');
        tbody.innerHTML = '';
        
        const tienePermisos = tienePermisosEdicion();
        
        cursos.forEach(curso => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${curso.id_curso}</td>
                <td>${curso.nombre}</td>
                <td>${curso.descripcion}</td>
                <td>${curso.id_profesor}</td>
                <td>
                    ${tienePermisos ? `
                        <button onclick="editarCurso(${curso.id_curso})" class="btn-editar">Editar</button>
                        <button onclick="eliminarCurso(${curso.id_curso})" class="btn-eliminar">Eliminar</button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        mostrarMensaje('Error al cargar cursos', 'error');
    }
}
