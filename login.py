import tkinter as tk
from tkinter import messagebox
import bcrypt

# Función para encriptar la contraseña
def encriptar_contrasena(contrasena):
    # Convertir la contraseña en bytes
    contrasena_bytes = contrasena.encode('utf-8')
    # Generar el hash de la contraseña con un salt
    salt = bcrypt.gensalt()
    hashed_contrasena = bcrypt.hashpw(contrasena_bytes, salt)
    return hashed_contrasena

# Función para verificar las credenciales
def verificar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Aquí simulamos un "usuario y contraseña" almacenados encriptados
    # En una aplicación real, estos deberían ser recuperados de una base de datos
    usuario_almacenado = "admin"
    contrasena_almacenada_hash = encriptar_contrasena("12345")

    # Comprobar si el usuario ingresado es correcto
    if usuario == usuario_almacenado:
        # Verificar si la contraseña proporcionada coincide con la encriptada
        if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_almacenada_hash):
            messagebox.showinfo("Éxito", "Login exitoso!")
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("300x200")  # Tamaño de la ventana

# Etiqueta y campo para el nombre de usuario
label_usuario = tk.Label(ventana, text="Usuario:")
label_usuario.pack(pady=5)

entry_usuario = tk.Entry(ventana)
entry_usuario.pack(pady=5)

# Etiqueta y campo para la contraseña
label_contrasena = tk.Label(ventana, text="Contraseña:")
label_contrasena.pack(pady=5)

entry_contrasena = tk.Entry(ventana, show="*")  # El '*' oculta la contraseña
entry_contrasena.pack(pady=5)

# Botón para verificar el login
boton_login = tk.Button(ventana, text="Iniciar sesión", command=verificar_login)
boton_login.pack(pady=20)

# Iniciar el loop de la ventana
ventana.mainloop()

