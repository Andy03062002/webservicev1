#HORA LOCAL TOMANDO LA UBICACION DEL SISTEMA 
from fastapi import FastAPI 
from datetime import datetime
from zoneinfo import ZoneInfo 

ahora = datetime.now()
ahora_actual = ahora.time()
app = FastAPI()

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
    return {"message":"hola"}




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