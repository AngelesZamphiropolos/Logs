# Conectarse a una base de datos
import sqlite3

# Abrir conexion con la base de datos, si no existe la crea
with sqlite3.connect("logs.db") as conexion:
    # Crear cursor (puente entre python y la base de datos)
    cursor = conexion.cursor()

    # Borra la tabla si existe
    cursor.execute("DROP TABLE IF EXISTS logs")

    # Crea la tabla logs
    cursor.execute("""
    CREATE TABLE logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        service TEXT NOT NULL,
        severity TEXT NOT NULL,
        message TEXT NOT NULL,
        received_at TEXT NOT NULL
    )
    """)

cursor.close()