# -*- coding: utf-8 -*-
# HORA LOCAL TOMANDO LA UBICACION DEL SISTEMA 
from fastapi import FastAPI 
from datetime import datetime
from zoneinfo import ZoneInfo 
from pydantic import BaseModel

# Modelos
class Texto(BaseModel):
    texto: str

class Cliente(BaseModel):
    id: int
    nombre: str
    correo: str

app = FastAPI()

# Diccionario de zonas horarias
ciudad_hora = {
    "CO": "America/Bogota",      # Colombia
    "EC": "America/Guayaquil",   # Ecuador
    "PE": "America/Lima",        # Perú
    "MX": "America/Mexico_City", # México
    "AR": "America/Argentina/Buenos_Aires", # Argentina
    "CL": "America/Santiago",    # Chile
    "VE": "America/Caracas",     # Venezuela
}

@app.get("/")
async def root():
    return {"message": "hola"}

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = ciudad_hora.get(iso)
    tz = ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.get("/temperatura/{escala}/{valor}")
async def temperatura(escala: str, valor: float):
    if escala.upper() == "C":
        resultado = (valor * 9/5) + 32
        return {"fahrenheit": round(resultado, 2)}
    elif escala.upper() == "F":
        resultado = (valor - 32) * 5/9
        return {"celsius": round(resultado, 2)}
    else:
        return {"error": "Usa C o F como escala"}

# Simulación de base de datos
db_clientes: list[Cliente] = []

@app.post("/clientes/", response_model=Cliente)
async def crear_cliente(cliente_info: Cliente):
    cliente = Cliente.model_validate(cliente_info.model_dump())
    db_clientes.append(cliente)
    return cliente

@app.get("/clientes/", response_model=list[Cliente])
async def listar_clientes():
    return db_clientes

@app.post("/analizar_texto")
async def analizar_texto(data: Texto):
    texto = data.texto.strip()
    palabras = texto.split()
    longitud = len(texto)
    cantidad_palabras = len(palabras)
    cantidad_vocales = sum(1 for c in texto.lower() if c in "aeiouaeiou")



    return {
        "texto_original": texto,
        "caracteres": longitud,
        "palabras": cantidad_palabras,
        "vocales": cantidad_vocales,
        "primera_palabra": palabras[0] if palabras else None,
        "ultima_palabra": palabras[-1] if palabras else None
    }
