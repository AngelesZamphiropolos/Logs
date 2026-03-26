# Para hacer peticiones HTTP
import requests
import random
# Para poder pausar el bucle de creación de logs
import time
# Para pasar en formato ISO 8601
from datetime import datetime

# URL del endpoint de la API 
servidor = "http://127.0.0.1:8000/logs"

# posibles niveles
nivel = ["info", "debug", "error", "warning"]

token = "token_A"

servicio = ["servicio1" , "servicio2"]

while True:
    # datetime.utcnow() fecha y hora actual
    # .isoformat() convierte en string con formato ISO 8601 (estándar internacional para escribir fechas y horas)
    log= {"timestamp": datetime.utcnow().isoformat(),
          # random.choice(lista) elige un elemento la lista
          "service": random.choice(servicio),
          "severity": random.choice(nivel),
          "message": f"Evento simulado {random.randint(1, 100)}"
        }
    
    # metadatos de la petición HTTP
    headers = {"Authorization": f"Token {token}"}
    
    try:
        respuesta= requests.post(servidor, json=log, headers=headers)
        print("enviado:", log,"respuesta:", respuesta.json())
        print("\n")
        
    except Exception as e:
        print("Error al enviar:", e)
    
    time.sleep(3)