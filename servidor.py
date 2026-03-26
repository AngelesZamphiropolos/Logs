# para ejecutar el objeto FastAPI
# uvicorn servidor:app --reload

# importar base de datos
import sqlite3
# framework a utilizar
from fastapi import FastAPI, Request, HTTPException, Query
# para trabajar con fechas y horas
from datetime import datetime
# para que tome como opcional algo
from typing import Optional

# instanciar la app que recibe las peticiones 
app = FastAPI()

# tokens válidos
tokens =  {
    "token_A" : "servicio_1",
    "token_B" : "servicio_2",
    "token_C" : "servicio_3" 
}

# guardar los logs en la base de datos
def guardar(timestamp, service, severity, message):
    # abrir la db
    conexion = sqlite3.connect("logs.db")

    # crear cursor
    cursor = conexion.cursor()

    # cargar el log a la db
    cursor.execute("""
        INSERT INTO logs (timestamp, service, severity, message, received_at)
        VALUES(?, ?, ?, ?, ?)""",
        (timestamp, service, severity, message, datetime.utcnow().isoformat()))

    conexion.commit()
    conexion.close()

# recibir y guardar
# crear el endpoint = punto de acceso al que un cliente puede enviar una petición y obtener una respuesta
@app.post("/logs")

# Request : objeto que contiene info del HTTP que envió el cliente (headers, get, post, url, etc.)
async def post_logs(request: Request):
    # leer header Authorization (permiso que el cliente tiene que traer para poder usar la API)
    autorizacion = request.headers.get("Authorization")
    
    # validar que exista y empiece con "Token "
    if not autorizacion or not autorizacion.startswith("Token "):
        # si no existe o el cliente no se identificó, lanzar una exception
        # 401 = El cliente no envió un token o ni siquiera intentó identificarse
        raise HTTPException(status_code=401, detail="Falta token")
    
    # ya que autorizacion cuenta con dos partes, entonces lo convertimos en lista y agarramos el segundo elemento, que sería el token
    token = autorizacion.split(" ", 1)[1]
    
    # comprobar si el token es válido
    if token not in tokens:
        # si no es válido, lanzar una exception
        # 403 = el cliente envió el token pero no tiene permiso
        raise HTTPException(status_code=403, detail="Quien sos, bro?")
    
    # leer el cuerpo JSON de la petición
    # permite esperar una operación que tarda sin congelar todo el servidor
    dato = await request.json() 
    
    # guardar en la base de datos
    guardar(dato["timestamp"], dato["service"], dato["severity"], dato["message"])
    
    return {"status": "ok", "saved": 1}

@app.get("/logs")
def get_logs(timestamp: Optional[datetime] = Query(None), severity: Optional[str] = Query(None)):
    
    # crear conexión con la db
    conexion = sqlite3.connect("logs.db")
    cursor = conexion.cursor()

    # consulta base, WHERE 1=1 para concatenar con AND después
    consulta = "SELECT * FROM logs WHERE 1=1"
    parametros = []

    # filtros para url válida
    if timestamp:
        consulta += " AND timestamp = ?"
        parametros.append(timestamp.isoformat())

    if severity:
        consulta += " AND severity = ?"
        parametros.append(severity)
    
    # ordenar los datos del más nuevo al más viejo
    consulta += " ORDER BY id DESC"
    
    # ejecutar la consulta
    cursor.execute(consulta, parametros)

    # obtener lo que devolvió el SELECT
    logs = cursor.fetchall()

    # cerrar la conexión 
    conexion.close()
    
    # retornar lo que devolvió la consulta
    return{"logs": logs}