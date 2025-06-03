from Estudiante import Estudiante
from GestionEstudiantes import GestionEstudiantes

# Crear instancia de la gestión
gestion = GestionEstudiantes()

# Crear algunos estudiantes
est1 = Estudiante(1, "Juan Pérez", "555-1234", "Alergia a penicilina", "Promedio: 9.0")
est2 = Estudiante(2, "Ana Gómez", "555-5678", "Sin alergias", "Promedio: 8.5")

# Agregar estudiantes
gestion.agregar_estudiante(est1)
gestion.agregar_estudiante(est2)

# Listar estudiantes
print("Lista de estudiantes:")
for est in gestion.listar_estudiantes():
    print(est.id_estudiante, est.nombre)

# Buscar un estudiante
estudiante = gestion.buscar_estudiante(1)
if estudiante:
    print("\nEstudiante encontrado:", estudiante.nombre)

# Modificar datos de un estudiante
gestion.modificar_estudiante(1, nombre="Juan P. Pérez", info_contacto="555-9999")
print("\nDatos actualizados:")
estudiante = gestion.buscar_estudiante(1)
print(estudiante.id_estudiante, estudiante.nombre, estudiante.info_contacto)

# Eliminar un estudiante
gestion.eliminar_estudiante(2)
print("\nLista después de eliminar:")
for est in gestion.listar_estudiantes():
    print(est.id_estudiante, est.nombre)