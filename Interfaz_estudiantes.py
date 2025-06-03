import tkinter as tk
from tkinter import messagebox
from Estudiante import Estudiante
from conexion_bd import ConexionBD
from GestionEstudiantes import GestionEstudiantes

# Configura la conexión y la gestión
conexion = ConexionBD(
    dbname="postgres",
    user="postgres",
    password="Pablo2l3l4l5",
    host="localhost",
    port=5433
)
conexion.conectar()
gestion_estudiantes = GestionEstudiantes(conexion)

def agregar_estudiante():
    nombre = entry_nombre.get()
    nombre_contacto = entry_nombre_contacto.get()
    relacion_contacto = entry_relacion_contacto.get()
    telefono_contacto = entry_telefono_contacto.get()
    datos_medicos = entry_medicos.get()
    datos_academicos = entry_academicos.get()
    
    if not nombre or not nombre_contacto or not telefono_contacto:
        messagebox.showerror("Error", "Nombre, nombre del contacto y teléfono son obligatorios.")
        return
        
    estudiante = Estudiante(None, nombre, nombre_contacto, relacion_contacto, 
                          telefono_contacto, datos_medicos, datos_academicos)
    if gestion_estudiantes.agregar_estudiante(estudiante):
        messagebox.showinfo("Éxito", "Estudiante agregado correctamente.")
        entry_nombre.delete(0, tk.END)
        entry_nombre_contacto.delete(0, tk.END)
        entry_relacion_contacto.delete(0, tk.END)
        entry_telefono_contacto.delete(0, tk.END)
        entry_medicos.delete(0, tk.END)
        entry_academicos.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "No se pudo agregar el estudiante.")

# Ventana principal
root = tk.Tk()
root.title("Gestión de Estudiantes")

tk.Label(root, text="Nombre:").grid(row=0, column=0, sticky="e")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Nombre del contacto:").grid(row=1, column=0, sticky="e")
entry_nombre_contacto = tk.Entry(root)
entry_nombre_contacto.grid(row=1, column=1)

tk.Label(root, text="Relación con el contacto:").grid(row=2, column=0, sticky="e")
entry_relacion_contacto = tk.Entry(root)
entry_relacion_contacto.grid(row=2, column=1)

tk.Label(root, text="Teléfono del contacto:").grid(row=3, column=0, sticky="e")
entry_telefono_contacto = tk.Entry(root)
entry_telefono_contacto.grid(row=3, column=1)

tk.Label(root, text="Datos médicos:").grid(row=4, column=0, sticky="e")
entry_medicos = tk.Entry(root)
entry_medicos.grid(row=4, column=1)

tk.Label(root, text="Datos académicos:").grid(row=5, column=0, sticky="e")
entry_academicos = tk.Entry(root)
entry_academicos.grid(row=5, column=1)

btn_agregar = tk.Button(root, text="Agregar Estudiante", command=agregar_estudiante)
btn_agregar.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
conexion.cerrar()