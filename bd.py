import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    contraseña = Column(String(100), nullable=False)
    rol = Column(String(20), nullable=False, default='colaborador')

    def __repr__(self):
        return f"<Usuario(nombre_usuario='{self.nombre_usuario}')>"

class Proyecto(Base):
    __tablename__ = 'proyectos'

    id_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)

    def __repr__(self):
        return f"<Proyecto(nombre='{self.nombre}')>"

class Tarea(Base):
    __tablename__ = 'tareas'

    id_tarea = Column(Integer, primary_key=True, autoincrement=True)
    id_proyecto = Column(Integer, ForeignKey('proyectos.id_proyecto'), nullable=False)
    descripcion = Column(String(255), nullable=False)
    fecha_vencimiento = Column(Date)
    id_usuario_asignado = Column(Integer, ForeignKey('usuarios.id_usuario'))
    estado = Column(String(20), nullable=False, default='pendiente')
    prioridad = Column(String(10), nullable=False, default='media')

    def __repr__(self):
        return f"<Tarea(descripcion='{self.descripcion}')>"

class MiembroProyecto(Base):
    __tablename__ = 'miembros_proyecto'

    id_proyecto = Column(Integer, ForeignKey('proyectos.id_proyecto'), primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), primary_key=True)
    rol = Column(String(20), nullable=False, default='colaborador')

    def __repr__(self):
        return f"<MiembroProyecto(id_proyecto='{self.id_proyecto}', id_usuario='{self.id_usuario}', rol='{self.rol}')>"

# Configuración de la base de datos MySQL
DB_HOST = 'localhost'
DB_NAME = 'gestion_proyectos_db'
DB_USER = 'root'
DB_PASSWORD = ''

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ejemplo de uso (fuera de la definición de la base de datos):
if __name__ == "__main__":
    # Nota: Asegúrate de que el servidor MySQL esté corriendo y que la base de datos 'gestion_proyectos_db' esté creada.
    
    # Crear las tablas (si no existen)
    Base.metadata.create_all(engine)

    db = SessionLocal()

    try:
        # Crear un nuevo usuario
        password_plain = "miclave123"
        hashed_password = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt())
        nuevo_usuario = Usuario(nombre_usuario="juan.perez", contraseña=hashed_password.decode('utf-8'), rol="administrador")
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        print("Usuario creado:", nuevo_usuario)

        # Crear un nuevo proyecto
        fecha_inicio = datetime.strptime("2025-04-15", "%Y-%m-%d").date()
        fecha_fin = datetime.strptime("2025-05-30", "%Y-%m-%d").date()
        nuevo_proyecto = Proyecto(nombre="Desarrollo Web", fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        db.add(nuevo_proyecto)
        db.commit()
        db.refresh(nuevo_proyecto)
        print("Proyecto creado:", nuevo_proyecto)

        # Crear una nueva tarea
        fecha_vencimiento = datetime.strptime("2025-04-22", "%Y-%m-%d").date()
        nueva_tarea = Tarea(id_proyecto=nuevo_proyecto.id_proyecto, descripcion="Implementar la página de inicio", fecha_vencimiento=fecha_vencimiento, id_usuario_asignado=nuevo_usuario.id_usuario, estado="pendiente", prioridad="alta")
        db.add(nueva_tarea)
        db.commit()
        db.refresh(nueva_tarea)
        print("Tarea creada:", nueva_tarea)

        # Asignar el usuario al proyecto
        nuevo_miembro = MiembroProyecto(id_proyecto=nuevo_proyecto.id_proyecto, id_usuario=nuevo_usuario.id_usuario, rol="desarrollador")
        db.add(nuevo_miembro)
        db.commit()
        print("Miembro asignado al proyecto:", nuevo_miembro)

        # Consultar todos los proyectos
        proyectos = db.query(Proyecto).all()
        print("\nProyectos:")
        for proyecto in proyectos:
            print(proyecto)

    finally:
        db.close()
