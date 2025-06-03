/**
 * Script para manejar la funcionalidad de inicio de sesión
 * Este archivo gestiona la autenticación de usuarios en el sistema
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicialización de variables principales
    const btnLogin = document.getElementById('btn-login');
    const mensajeError = document.getElementById('mensaje-error');
    
    /**
     * Funcionalidad para mostrar/ocultar contraseña
     * Permite al usuario alternar la visibilidad de la contraseña
     */
    const togglePassword = document.getElementById('toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = document.getElementById('contrasena');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.textContent = '👁️‍🗨️'; // Ojo con línea (indicando que la contraseña es visible)
            } else {
                passwordInput.type = 'password';
                this.textContent = '👁️'; // Ojo normal (indicando que la contraseña está oculta)
            }
        });
    }
    
    // Asignar evento de clic al botón de inicio de sesión
    btnLogin.addEventListener('click', iniciarSesion);
    
    /**
     * Permitir iniciar sesión presionando Enter en el campo de contraseña
     * Mejora la experiencia de usuario al no requerir clic en el botón
     */
    document.getElementById('contrasena').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            iniciarSesion();
        }
    });
    
    /**
     * Función principal para iniciar sesión
     * Valida los campos, envía la petición al servidor y maneja la respuesta
     */
    function iniciarSesion() {
        // Obtener y limpiar valores de los campos
        const nombreUsuario = document.getElementById('nombre_usuario').value.trim();
        const contrasena = document.getElementById('contrasena').value.trim();
        
        // Validación básica de campos vacíos
        if (!nombreUsuario || !contrasena) {
            mostrarError('Por favor, complete todos los campos');
            return;
        }
        
        // Deshabilitar botón durante la petición para evitar múltiples envíos
        btnLogin.disabled = true;
        btnLogin.textContent = 'Iniciando sesión...';
        
        /**
         * Enviar petición al servidor mediante fetch API
         * Utiliza método POST con JSON para enviar credenciales
         */
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre_usuario: nombreUsuario,
                contrasena: contrasena
            })
        })
        .then(response => {
            // Verificar si la respuesta es correcta
            if (!response.ok) {
                throw new Error(`Error HTTP ${response.status}`);
            }
            // Verificar que la respuesta sea JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new TypeError('La respuesta no es JSON');
            }
            return response.json();
        })
        .then(data => {
            // Procesar respuesta exitosa
            if (data.exito) {
                // Guardar el rol del usuario en localStorage para usarlo en index.html
                localStorage.setItem('rol_usuario', data.rol);
                window.location.href = '/index';
            } else {
                // Mostrar mensaje de error y limpiar campo de contraseña
                mostrarError(data.mensaje || 'Error desconocido');
                document.getElementById('contrasena').value = '';
            }
        })
        .catch(error => {
            // Manejar errores de la petición
            console.error('Error:', error);
            // Personalizar mensaje según tipo de error
            const mensaje = error.message.includes('404') ? 'Endpoint no encontrado' : 
                          error.message.includes('JSON') ? 'Error en formato de respuesta' : 
                          'Error de conexión';
            mostrarError(mensaje);
        })
        .finally(() => {
            // Restaurar botón independientemente del resultado
            btnLogin.disabled = false;
            btnLogin.textContent = 'Iniciar Sesión';
        });
    }
    
    /**
     * Función para mostrar mensajes de error
     * Muestra el mensaje y lo oculta automáticamente después de 3 segundos
     * @param {string} mensaje - Texto del mensaje de error a mostrar
     */
    function mostrarError(mensaje) {
        mensajeError.textContent = mensaje;
        mensajeError.style.opacity = 1;
        
        // Hacer que el mensaje desaparezca después de 3 segundos
        setTimeout(() => {
            mensajeError.style.opacity = 0;
        }, 3000);
    }
});