import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from bd import Usuario
import bcrypt

# Conexion a la base de datos
DB_HOST = 'localhost'
DB_NAME = 'gestion_proyectos_db'
DB_USER = 'root'
DB_PASSWORD = ''

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funciones Login
def verificar_login(username, password):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.contraseña.encode('utf-8')):
            return True
        else:
            return False
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"Hubo un problema al conectar a la base de datos: {str(e)}")
        return False
    finally:
        db.close()

# Función para manejar el evento de login
def login():
    username = entry_username.get()
    password = entry_password.get()

    if verificar_login(username, password):
        messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
        root.destroy()  # Cierra la ventana de login al iniciar sesión
        # Aquí podrías abrir la siguiente ventana de tu aplicación
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

# Función para crear un nuevo usuario
def crear_usuario():
    def guardar_usuario():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()
        new_role = entry_new_role.get()

        if new_username and new_password and new_role:
            # Verificar si el nombre de usuario ya existe
            db = SessionLocal()
            existing_user = db.query(Usuario).filter(Usuario.nombre_usuario == new_username).first()

            if existing_user:
                messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
            else:
                # Crear un nuevo usuario
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                new_user = Usuario(nombre_usuario=new_username, contraseña=hashed_password.decode('utf-8'), rol=new_role)
                db.add(new_user)
                db.commit()
                db.close()
                messagebox.showinfo("Éxito", "¡Usuario creado exitosamente!")
                create_window.destroy()  # Cierra la ventana de creación de usuario
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    # Ventana para crear nuevo usuario
    create_window = tk.Toplevel(root)
    create_window.title("Crear Nuevo Usuario")

    label_new_username = tk.Label(create_window, text="Nombre de usuario:")
    label_new_username.pack(pady=5)
    entry_new_username = tk.Entry(create_window)
    entry_new_username.pack(pady=5)

    label_new_password = tk.Label(create_window, text="Contraseña:")
    label_new_password.pack(pady=5)
    entry_new_password = tk.Entry(create_window, show="*")
    entry_new_password.pack(pady=5)

    label_new_role = tk.Label(create_window, text="Rol:")
    label_new_role.pack(pady=5)
    entry_new_role = tk.Entry(create_window)
    entry_new_role.pack(pady=5)

    button_save_user = tk.Button(create_window, text="Guardar Usuario", command=guardar_usuario)
    button_save_user.pack(pady=10)

# Crear la ventana de Tkinter
root = tk.Tk()
root.title("Login - Sistema de Gestión de Proyectos")

# Configurar el tamaño de la ventana
root.geometry("300x250")

# Etiquetas y campos de texto
label_username = tk.Label(root, text="Nombre de usuario:")
label_username.pack(pady=10)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Contraseña:")
label_password.pack(pady=10)

entry_password = tk.Entry(root, show="*")  # 'show' oculta la contraseña
entry_password.pack(pady=5)

# Botón de inicio de sesión
login_button = tk.Button(root, text="Iniciar sesión", command=login)
login_button.pack(pady=10)

# Botón para crear un nuevo usuario
create_user_button = tk.Button(root, text="Crear nuevo usuario", command=crear_usuario)
create_user_button.pack(pady=10)

# Ejecutar la ventana
root.mainloop()
