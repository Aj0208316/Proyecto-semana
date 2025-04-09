import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from bd import Usuario, Proyecto, Tarea, MiembroProyecto # Asegúrate de que 'bd' es el archivo que contiene los modelos de SQLAlchemy
import bcrypt

# Configuración de la base de datos
DB_HOST = 'localhost'
DB_NAME = 'gestion_proyectos_db'
DB_USER = 'root'
DB_PASSWORD = ''

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función de verificación de login
def verificar_login(username, password):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.contraseña.encode('utf-8')):
            return usuario  # Retorna el objeto usuario si la autenticación es exitosa
        else:
            return None  # Si el usuario o la contraseña no son correctos
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"Hubo un problema al conectar a la base de datos: {str(e)}")
        return None
    finally:
        db.close()

# Función de login
def login():
    username = entry_username.get()
    password = entry_password.get()

    usuario = verificar_login(username, password)
    if usuario:
        messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
        login_window.destroy()  # Cierra la ventana de login al iniciar sesión
        mostrar_panel_principal(usuario)  # Llama a la función para mostrar el panel principal
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")


# Función para cerrar sesión
def cerrar_sesion():
    global root
    messagebox.showinfo("Cerrar sesión", "Has cerrado sesión correctamente.")
    root.quit()  # Finaliza la ejecución de la aplicación

# Función para cargar los proyectos y tareas del usuario
# Función para cargar los proyectos y tareas del usuario
def cargar_datos(usuario):
    db = SessionLocal()
    
    # Obtener los proyectos en los que el usuario está involucrado a través de la tabla MiembroProyecto
    proyectos = db.query(Proyecto).join(MiembroProyecto).filter(MiembroProyecto.id_usuario == usuario.id_usuario).all()
    
    # Obtener las tareas asignadas a este usuario
    tareas = db.query(Tarea).filter(Tarea.id_usuario_asignado == usuario.id_usuario).all()

    # Limpiar las tablas antes de llenarlas con nuevos datos
    for item in tree_proyectos.get_children():
        tree_proyectos.delete(item)
    for item in tree_tareas.get_children():
        tree_tareas.delete(item)

    # Llenar la tabla de proyectos
    for proyecto in proyectos:
        tree_proyectos.insert("", "end", values=(proyecto.id_proyecto, proyecto.nombre, proyecto.fecha_inicio, proyecto.fecha_fin))
    
    # Llenar la tabla de tareas
    for tarea in tareas:
        tree_tareas.insert("", "end", values=(tarea.id_tarea, tarea.descripcion, tarea.estado, tarea.prioridad))



# Función para mostrar el panel principal
def mostrar_panel_principal(usuario):
    global root
    root = tk.Tk()
    root.title("Gestor de Tareas - Panel Principal")
    root.geometry("800x600")

    # Encabezado
    frame_top = tk.Frame(root, bg="#e0ffe0", height=50)
    frame_top.pack(fill="x")
    tk.Label(frame_top, text=f"👤 Usuario: {usuario.nombre_usuario}", bg="#e0ffe0", font=("Arial", 12)).pack(side="left", padx=10)
    tk.Button(frame_top, text="Cerrar sesión", command=cerrar_sesion).pack(side="right", padx=10)

    # Botones principales
    frame_buttons = tk.Frame(root, pady=10)
    frame_buttons.pack()
    tk.Button(frame_buttons, text="➕ Nuevo Proyecto", width=20).grid(row=0, column=0, padx=10)
    tk.Button(frame_buttons, text="📝 Nueva Tarea", width=20).grid(row=0, column=1, padx=10)
    tk.Button(frame_buttons, text="📈 Ver Progreso", width=20).grid(row=0, column=2, padx=10)

    # Tabla de proyectos
    tk.Label(root, text="📁 Proyectos", font=("Arial", 12, "bold")).pack(pady=(20, 5))
    tree_proyectos = ttk.Treeview(root, columns=("ID", "Nombre", "Inicio", "Fin"), show="headings")
    for col in tree_proyectos["columns"]:
        tree_proyectos.heading(col, text=col)
    tree_proyectos.pack(pady=5, fill="x")

    # Tabla de tareas
    tk.Label(root, text="📋 Tareas Asignadas", font=("Arial", 12, "bold")).pack(pady=(20, 5))
    tree_tareas = ttk.Treeview(root, columns=("ID", "Descripción", "Estado", "Prioridad"), show="headings")
    for col in tree_tareas["columns"]:
        tree_tareas.heading(col, text=col)
    tree_tareas.pack(pady=5, fill="x")

    # Cargar proyectos y tareas del usuario
    cargar_datos(usuario)

    root.mainloop()

# Crear la ventana de login
login_window = tk.Tk()
login_window.title("Login - Sistema de Gestión de Proyectos")
login_window.geometry("300x200")

# Etiquetas y campos de texto para login
label_username = tk.Label(login_window, text="Nombre de usuario:")
label_username.pack(pady=10)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

label_password = tk.Label(login_window, text="Contraseña:")
label_password.pack(pady=10)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=5)

# Botón de inicio de sesión
login_button = tk.Button(login_window, text="Iniciar sesión", command=login)
login_button.pack(pady=20)

# Ejecutar la ventana de login
login_window.mainloop()
