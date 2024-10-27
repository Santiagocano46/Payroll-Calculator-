"""
    Pertenece a la capa de Acceso a Datos

    Controla las operaciones de almacenamiento de la clase Usuario
"""
import sys
sys.path.append("src")
from logic.payroll_calculator import Usuario
import psycopg2
import SecretConfig

def ObtenerCursor( ) :
    """
    Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones
    """
    DATABASE = SecretConfig.PGDATABASE
    USER = SecretConfig.PGUSER
    PASSWORD = SecretConfig.PGPASSWORD
    HOST = SecretConfig.PGHOST
    PORT = SecretConfig.PGPORT
    connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return connection.cursor()

#Crear Tabla

def CrearTabla():
    """
    Crea la tabla de usuarios, en caso de que no exista
    """    
    sql = ""
    with open("sql/crear-usuarios.sql","r") as f:
        sql = f.read()

    cursor = ObtenerCursor()
    try:
        cursor.execute( sql )
        cursor.connection.commit()
    except:
        cursor.connection.rollback()

#Insertar datos en la BD

def Insertar( usuario : Usuario ):
    """ Guarda un Usuario en la base de datos """

    try:
        cursor = ObtenerCursor()
        cursor.execute(f"""
        insert into usuarios (
            cedula, nombre,  salario,  dias_trabajados,  horas_trabajadas, comisiones, horas_extras)
        values 
        (
            '{usuario.cedula}',  '{usuario.nombre}', '{usuario.salary}', '{usuario.days_worked}', '{usuario.hours_worked}', '{usuario.commissions}', '{usuario.overtime_hours}'
        );
                        """)
        
        cursor.connection.commit()
    except:
        cursor.connection.rollback() 
        raise Exception(f"No fue posible insertar el usuario : {usuario.cedula} ")
    
#Modificar Datos
    
def Actualizar(usuario: Usuario):
    """
    Actualiza los datos de un usuario en la base de datos.
    """
    cursor = ObtenerCursor()
    try:
        cursor.execute(f"""
            update usuarios
            set 
                nombre='{usuario.nombre}',
                salario='{usuario.salary}',
                dias_trabajados='{usuario.days_worked}',
                horas_trabajadas='{usuario.hours_worked}',
                comisiones='{usuario.commissions}',
                horas_extras='{usuario.overtime_hours}'
            where cedula='{usuario.cedula}'
        """)
        cursor.connection.commit()
    *
        cursor.connection.rollback()
        raise e



#Delete
def Borrar(cedula: str):
    """ Elimina la fila que contiene a un usuario en la BD """
    cursor = ObtenerCursor()
    try:
        sql = f"DELETE from usuarios where cedula = '{cedula}'"
        cursor.execute(sql)
        cursor.connection.commit()
    except Exception as e:
        cursor.connection.rollback()
        raise e


#Consultar Datos 

def BuscarPorCedula(cedula: str):
    """ Busca un usuario por el número de Cedula """
    cursor = ObtenerCursor()
    
    try:
        cursor.execute("""
            SELECT cedula, nombre, salario, dias_trabajados, horas_trabajadas, comisiones, horas_extras 
            FROM usuarios 
            WHERE cedula = %s
        """, (cedula,))
        
        fila = cursor.fetchone()
        
        if fila is None:
            return f"No se encontró un usuario con la cédula: {cedula}"
        
        msg = (f"El usuario que tiene por cédula: {fila[0]}, nombre: {fila[1]}, salario: {fila[2]}, "
               f"dias_trabajados: {fila[3]}, horas_trabajadas: {fila[4]}, comisiones: {fila[5]}, "
               f"horas_extras: {fila[6]}")
        return msg
    
    except Exception as e:
        return f"Error al buscar usuario: {e}"
    
    finally:
        cursor.close()
