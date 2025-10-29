# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from gmail_client import enviar_correo

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class Usuario(BaseModel):
    nombres: str
    edad: int
    correo: str
    usuario: str
    password: str

class LoginRequest(BaseModel):
    usuario: str
    password: str

# Conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="fitdb"
    )

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}

# Endpoint: Registrar usuario
@app.post("/register")
async def register(data: Usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nombres, edad, correo, usuario, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (data.nombres, data.edad, data.correo, data.usuario, data.password))
        conn.commit()
        cursor.close()
        conn.close()

        # Enviar correo de notificación
        asunto = "Registro Exitoso - 17Fitness"
        cuerpo = f"Hola {data.nombres},\n\nTu registro en el sistema de rutinas personalizadas ha sido exitoso.\n¡Bienvenido a 17Fitness!"
        enviar_correo(data.correo, asunto, cuerpo)

        return {"status": "success", "message": f"Usuario {data.usuario} registrado correctamente y correo enviado."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Endpoint: Login
@app.post("/login")
async def login(data: LoginRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM usuarios WHERE correo = %s AND password = %s"
        cursor.execute(sql, (data.usuario, data.password))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Enviar correo de notificación
            asunto = "Inicio de Sesión Detectado - 17Fitness"
            cuerpo = f"Hola {user['nombres']},\n\nSe ha detectado un nuevo inicio de sesión en tu cuenta de 17Fitness."
            enviar_correo(user['correo'], asunto, cuerpo)

            return {"status": "success", "message": f"Inicio de sesión exitoso. Bienvenido, {user['nombres']}!"}
        else:
            return {"status": "error", "message": "Usuario o contraseña incorrectos"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
