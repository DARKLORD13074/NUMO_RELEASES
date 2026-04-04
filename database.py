import os
from dotenv import load_dotenv
import mysql.connector
import bcrypt

load_dotenv()

def conectar_bd():
    """Establece la conexión con MySQL."""
    try:
        conexion = mysql.connector.connect(
            host= os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            port=int(os.getenv("DB_PORT")),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None

def obtener_datos_jugador(id_jugador=1):
    """Obtiene toda la fila del jugador especificado y la devuelve como diccionario."""
    conexion = conectar_bd()
    if conexion:
        # dictionary=True hace que los resultados se devuelvan como un diccionario de Python
        cursor = conexion.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM progreso_jugadores WHERE id = %s", (id_jugador,))
        resultado = cursor.fetchone() # Trae solo el primer resultado
        
        cursor.close()
        conexion.close()
        return resultado
    return None

def actualizar_recursos(id_jugador, vidas, diamantes):
    """Guarda la cantidad actual de vidas y diamantes."""
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        sql = "UPDATE progreso_jugadores SET vidas = %s, diamantes = %s WHERE id = %s"
        cursor.execute(sql, (vidas, diamantes, id_jugador))
        conexion.commit() 
        cursor.close()
        conexion.close()

def actualizar_perfil_bd(id_jugador, usuario, descripcion, avatar_icono, avatar_color):
    """Guarda los cambios hechos en la pantalla de perfil."""
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        sql = "UPDATE progreso_jugadores SET usuario = %s, descripcion = %s, avatar_icono = %s, avatar_color = %s WHERE id = %s"
        cursor.execute(sql, (usuario, descripcion, avatar_icono, avatar_color, id_jugador))
        conexion.commit()
        cursor.close()
        conexion.close()

def actualizar_progreso_juego(id_jugador, niveles_completados, xp_total):
    """Guarda el progreso de niveles y la XP acumulada en la base de datos."""
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        sql = "UPDATE progreso_jugadores SET niveles_completados = %s, xp_total = %s WHERE id = %s"
        cursor.execute(sql, (niveles_completados, xp_total, id_jugador))
        conexion.commit()
        cursor.close()
        conexion.close()
        
def registrar_jugador(email, usuario, password_plana):
    """Registra un nuevo jugador en la base de datos con contraseña encriptada."""
    conexion = conectar_bd()
    if not conexion:
        return False, "Error de conexión a la base de datos."

    cursor = conexion.cursor(dictionary=True)
    
    # 1. Verificar si el correo o usuario ya existen
    cursor.execute("SELECT * FROM progreso_jugadores WHERE email = %s OR usuario = %s", (email, usuario))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return False, "El correo o el nombre de usuario ya están registrados."

    # 2. Encriptar la contraseña
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_plana.encode('utf-8'), salt).decode('utf-8')

    # 3. Lógica del creador (Insignia de Fundador)
    CORREO_CREADOR = "ander12393.a@gmail.com"
    insignias_iniciales = "fundador,novato" if email == CORREO_CREADOR else "novato"

    sql_insert = """
        INSERT INTO progreso_jugadores 
        (email, usuario, password, descripcion, niveles_completados, xp_total, insignias, vidas, diamantes, avatar_icono, avatar_color) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (email, usuario, password_hash, "Nuevo estudiante en Numo", 0, 0, insignias_iniciales, 5, 450, "ACCOUNT_CIRCLE", "blue")
    
    try:
        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Registro exitoso."
    except Exception as e:
        return False, f"Error al registrar: {e}"
    finally:
        cursor.close()
        conexion.close()


def autenticar_jugador(identificador, password_plana):
    """Verifica las credenciales del usuario (email o nombre de usuario)."""
    conexion = conectar_bd()
    if not conexion:
        return None, "Error de conexión a la base de datos."

    # PARCHE 1: Agregamos buffered=True para evitar el error "Unread result found"
    cursor = conexion.cursor(dictionary=True, buffered=True) 
    
    # Buscamos por email o por nombre de usuario
    cursor.execute("SELECT * FROM progreso_jugadores WHERE email = %s OR usuario = %s", (identificador, identificador))
    jugador = cursor.fetchone()
    
    cursor.close()
    conexion.close()

    if jugador:
        password_guardada = jugador.get('password')
        
        # PARCHE 2: Evitamos que la app colapse si la cuenta es antigua y no tiene contraseña
        if not password_guardada:
            return None, "Esta cuenta es antigua. Por favor, ve a 'Registrarse' y créala de nuevo para actualizarla."

        # Verificamos si la contraseña coincide con el hash guardado
        if bcrypt.checkpw(password_plana.encode('utf-8'), password_guardada.encode('utf-8')):
            return jugador, "Login exitoso."
        else:
            return None, "Contraseña incorrecta."
    
    return None, "Usuario no encontrado."

def imprimir_todos_los_jugadores():
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM progreso_jugadores")
        jugadores = cursor.fetchall() # Trae todos los registros
        
        print("\n--- DATOS EN LA BASE DE DATOS ---")
        for j in jugadores:
            print(f"ID: {j['id']} | Usuario: {j['usuario']} | XP: {j['xp_total']} | Vidas: {j['vidas']}")
        
        cursor.close()
        conexion.close()

def obtener_leaderboard():
    """Obtiene el top 50 de jugadores ordenados por XP."""
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        # Cambia 'xp_total' por 'xp_semanal' cuando actualices tu esquema SQL
        cursor.execute("""
            SELECT id, usuario, xp_total, avatar_icono, avatar_color, insignias, descripcion, niveles_completados
            FROM progreso_jugadores 
            ORDER BY xp_total DESC 
            LIMIT 50
        """)
        jugadores = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jugadores
    return []

# Llamar a la función para probar
if __name__ == "__main__":
    imprimir_todos_los_jugadores()