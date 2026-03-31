from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis

# 1. Inicializamos la API y la conexión a Redis (en WSL/localhost)
app = FastAPI()
db = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 2. Definimos qué datos esperamos recibir del cliente
class UnnumberedRequest(BaseModel):
    client_id: str
    request_id: str

class NumberedRequest(BaseModel):
    client_id: str
    seat_id: str
    request_id: str

# 3. Endpoint para comprar entradas NO numeradas
@app.post("/buy/unnumbered")
def buy_unnumbered(req: UnnumberedRequest):
    # Restamos 1 al contador de entradas disponibles de forma atómica
    quedan = db.decr('tickets_disponibles')
    
    if quedan >= 0:
        # Éxito: Aún quedaban entradas
        return {"status": "success", "message": f"Ticket purchased. Remaining: {quedan}"}
    else:
        # Fallo: Se han agotado
        # Volvemos a sumar 1 para que el contador no baje a números negativos infinitos
        db.incr('tickets_disponibles')
        raise HTTPException(status_code=400, detail="Tickets sold out")

# 4. Endpoint para comprar entradas numeradas
@app.post("/buy/numbered")
def buy_numbered(req: NumberedRequest):
    # Creamos una clave única para el asiento, ej: "asiento:42"
    clave_asiento = f"asiento:{req.seat_id}"
    
    # SETNX intentará guardar el client_id en ese asiento.
    # Devuelve 1 (True) si lo logra, o 0 (False) si ya existía.
    exito = db.setnx(clave_asiento, req.client_id)
    
    if exito:
        return {"status": "success", "message": f"Seat {req.seat_id} purchased"}
    else:
        # Si devuelve False, alguien más fue más rápido
        raise HTTPException(status_code=400, detail="Seat already sold")