from GestionEstudiantes import GestionEstudiantes
from GestionProfesores import GestionProfesores
from GestionCursos import GestionCursos
from Estudiante import Estudiante
from Profesor import Profesor
from Curso import Curso

# Función principal del menú
def menu():
    # Instancias de las clases de gestión
    gestion_estudiantes = GestionEstudiantes()
    gestion_profesores = GestionProfesores()
    gestion_cursos = GestionCursos()

    while True:
        print(Fore.CYAN + "\n--- Menú Principal ---" + Style.RESET_ALL)
        print("1. Gestionar Estudiantes")
        print("2. Gestionar Profesores")
        print("3. Gestionar Cursos")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_estudiantes(gestion_estudiantes)
        elif opcion == "2":
            menu_profesores(gestion_profesores)
        elif opcion == "3":
            menu_cursos(gestion_cursos)
        elif opcion == "4":
            print(Fore.GREEN + "¡Hasta luego!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opción no válida." + Style.RESET_ALL)

# Submenú para gestión de estudiantes
def menu_estudiantes(gestion):
    while True:
        print("\n--- Gestión de Estudiantes ---")
        print("1. Agregar estudiante")
        print("2. Listar estudiantes")
        print("3. Modificar estudiante")
        print("4. Eliminar estudiante")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Solicita datos del nuevo estudiante
            id_estudiante = int(input("ID: "))
            nombre = input("Nombre: ")
            info_contacto = input("Información de contacto: ")
            datos_medicos = input("Datos médicos: ")
            datos_academicos = input("Datos académicos: ")
            # Crea y agrega el estudiante
            estudiante = Estudiante(id_estudiante, nombre, info_contacto, datos_medicos, datos_academicos)
            gestion.agregar_estudiante(estudiante)
            print("Estudiante agregado.")
        elif opcion == "2":
            # Lista todos los estudiantes
            print("\nLista de estudiantes:")
            for est in gestion.listar_estudiantes():
                print(est.id_estudiante, est.nombre)
        elif opcion == "3":
            # Solicita el ID y los nuevos datos para modificar un estudiante
            id_estudiante = int(input("ID del estudiante a modificar: "))
            nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            info_contacto = input("Nueva información de contacto (dejar vacío para no cambiar): ")
            datos_medicos = input("Nuevos datos médicos (dejar vacío para no cambiar): ")
            datos_academicos = input("Nuevos datos académicos (dejar vacío para no cambiar): ")
            gestion.modificar_estudiante(
                id_estudiante,
                nombre if nombre else None,
                info_contacto if info_contacto else None,
                datos_medicos if datos_medicos else None,
                datos_academicos if datos_academicos else None
            )
            print("Estudiante modificado.")
        elif opcion == "4":
            # Elimina un estudiante por ID
            id_estudiante = int(input("ID del estudiante a eliminar: "))
            if gestion.eliminar_estudiante(id_estudiante):
                print("Estudiante eliminado.")
            else:
                print("Estudiante no encontrado.")
        elif opcion == "5":
            # Vuelve al menú principal
            break
        else:
            print("Opción no válida.")

# Submenú para gestión de profesores
def menu_profesores(gestion):
    while True:
        print("\n--- Gestión de Profesores ---")
        print("1. Agregar profesor")
        print("2. Listar profesores")
        print("3. Modificar profesor")
        print("4. Eliminar profesor")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Solicita datos del nuevo profesor
            id_profesor = int(input("ID: "))
            nombre = input("Nombre: ")
            info_contacto = input("Información de contacto: ")
            # Crea y agrega el profesor
            profesor = Profesor(id_profesor, nombre, info_contacto)
            gestion.agregar_profesor(profesor)
            print("Profesor agregado.")
        elif opcion == "2":
            # Lista todos los profesores
            print("\nLista de profesores:")
            for prof in gestion.listar_profesores():
                print(prof.id_profesor, prof.nombre)
        elif opcion == "3":
            # Solicita el ID y los nuevos datos para modificar un profesor
            id_profesor = int(input("ID del profesor a modificar: "))
            nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            info_contacto = input("Nueva información de contacto (dejar vacío para no cambiar): ")
            gestion.modificar_profesor(
                id_profesor,
                nombre if nombre else None,
                info_contacto if info_contacto else None
            )
            print("Profesor modificado.")
        elif opcion == "4":
            # Elimina un profesor por ID
            id_profesor = int(input("ID del profesor a eliminar: "))
            if gestion.eliminar_profesor(id_profesor):
                print("Profesor eliminado.")
            else:
                print("Profesor no encontrado.")
        elif opcion == "5":
            # Vuelve al menú principal
            break
        else:
            print("Opción no válida.")

# Submenú para gestión de cursos
def menu_cursos(gestion):
    while True:
        print("\n--- Gestión de Cursos ---")
        print("1. Agregar curso")
        print("2. Listar cursos")
        print("3. Modificar curso")
        print("4. Eliminar curso")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Solicita datos del nuevo curso
            id_curso = int(input("ID: "))
            nombre = input("Nombre: ")
            descripcion = input("Descripción: ")
            id_profesor = int(input("ID del profesor: "))
            # Crea y agrega el curso
            curso = Curso(id_curso, nombre, descripcion, id_profesor)
            gestion.agregar_curso(curso)
            print("Curso agregado.")
        elif opcion == "2":
            # Lista todos los cursos
            print("\nLista de cursos:")
            for curso in gestion.listar_cursos():
                print(curso.id_curso, curso.nombre)
        elif opcion == "3":
            # Solicita el ID y los nuevos datos para modificar un curso
            id_curso = int(input("ID del curso a modificar: "))
            nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            descripcion = input("Nueva descripción (dejar vacío para no cambiar): ")
            id_profesor = input("Nuevo ID de profesor (dejar vacío para no cambiar): ")
            gestion.modificar_curso(
                id_curso,
                nombre if nombre else None,
                descripcion if descripcion else None,
                int(id_profesor) if id_profesor else None
            )
            print("Curso modificado.")
        elif opcion == "4":
            # Elimina un curso por ID
            id_curso = int(input("ID del curso a eliminar: "))
            if gestion.eliminar_curso(id_curso):
                print("Curso eliminado.")
            else:
                print("Curso no encontrado.")
        elif opcion == "5":
            # Vuelve al menú principal
            break
        else:
            print("Opción no válida.")

# Punto de entrada del programa
if __name__ == "__main__":
    menu()