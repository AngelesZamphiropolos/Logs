# API de Recolección de Logs

*Un proyecto backend simple y funcional para recibir, almacenar y consultar logs de servicios.*

## Descripción

Este proyecto implementa una pequeña API desarrollada con **FastAPI** que permite:

- recibir logs desde un cliente externo,
- validarlos mediante **token de autorización**,
- almacenarlos en una base de datos **SQLite**,
- y consultarlos con filtros básicos.

Además, incluye un script que simula eventos automáticamente, ideal para probar el flujo completo del sistema.

## Características

- Recepción de logs mediante `POST /logs`
- Autenticación básica con token
- Almacenamiento en SQLite
- Consulta de logs con filtros por `timestamp` y `severity`
- Script generador de eventos para pruebas
- Inicialización rápida de la base de datos

## Tecnologías utilizadas

- Python
- FastAPI
- SQLite
- Requests
- Uvicorn

## Estructura del proyecto

```bash
crear_bd.py   # Crea la base de datos y la tabla de logs
servidor.py   # API principal con los endpoints
servicio.py   # Cliente que simula y envía logs al servidor
```

## Cómo ejecutar el proyecto

```bash
pip install fastapi uvicorn requests
python crear_bd.py
uvicorn servidor:app --reload
python servicio.py
```

## Endpoints principales

### `POST /logs`
Recibe un log en formato JSON usando el header:

```bash
Authorization: Token token_A
```

### `GET /logs`
Devuelve los logs almacenados y permite aplicar filtros como:

```bash
/logs?severity=error
/logs?timestamp=2025-11-26T19:25:26.086488
```

## ¿Qué demuestra este proyecto?

Este proyecto reúne conceptos importantes de backend en una sola implementación:

- manejo de peticiones HTTP,
- validación de acceso,
- persistencia en base de datos,
- y consumo de API desde un cliente externo.

---

Proyecto pensado como práctica de desarrollo backend, con una estructura clara, lógica simple y una base sólida para seguir ampliándolo.
