import requests
import redis
import time

def leer_benchmark_unnumbered(ruta_archivo):
    peticiones = []
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'): continue
            partes = linea.split()
            if partes[0] == 'BUY':
                peticiones.append({'client_id': partes[1], 'request_id': partes[2]})
    return peticiones

def leer_benchmark_numbered(ruta_archivo):
    peticiones = []
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'): continue
            partes = linea.split()
            if partes[0] == 'BUY':
                peticiones.append({
                    'client_id': partes[1], 
                    'seat_id': partes[2], 
                    'request_id': partes[3]
                })
    return peticiones

def limpiar_base_de_datos():
    """Borra todo en Redis para empezar de cero entre pruebas."""
    db = redis.Redis(host='localhost', port=6379, decode_responses=True)
    db.flushdb() # Vacía la base de datos por completo
    print("🧹 Base de datos limpiada.")
    return db

def lanzar_peticiones(peticiones, url_endpoint):
    exitos = 0
    fallos = 0
    print(f"🚀 Iniciando envío de {len(peticiones)} peticiones a {url_endpoint}...")
    inicio = time.time()

    with requests.Session() as session:
        for peticion in peticiones:
            respuesta = session.post(url_endpoint, json=peticion)
            if respuesta.status_code == 200:
                exitos += 1
            else:
                fallos += 1

    fin = time.time()
    print("\n--- 📊 RESULTADOS ---")
    print(f"✅ Compras exitosas: {exitos}")
    print(f"❌ Compras fallidas (rechazadas por BD): {fallos}")
    print(f"⏱️ Tiempo total: {fin - inicio:.2f} segundos")
    print(f"⚡ Rendimiento: {len(peticiones) / (fin - inicio):.2f} pet/seg\n")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    db = limpiar_base_de_datos()
    
    # --- PRUEBA 1: UNNUMBERED ---
    print("=== TEST 1: ENTRADAS NO NUMERADAS ===")
    db.set('tickets_disponibles', 20000)
    peticiones_un = leer_benchmark_unnumbered('benchmark_unnumbered_20000.txt')
    lanzar_peticiones(peticiones_un, "http://127.0.0.1:80/buy/unnumbered")

    # --- PRUEBA 2: NUMBERED (NORMAL) ---
    print("=== TEST 2: ENTRADAS NUMERADAS ===")
    db = limpiar_base_de_datos()
    peticiones_num = leer_benchmark_numbered('benchmark_numbered_60000.txt')
    lanzar_peticiones(peticiones_num, "http://127.0.0.1:80/buy/numbered")

    # --- PRUEBA 3: NUMBERED (HOTSPOT) ---
    print("=== TEST 3: ENTRADAS NUMERADAS (HOTSPOT) 🔥 ===")
    db = limpiar_base_de_datos()
    peticiones_hotspot = leer_benchmark_numbered('benchmark_hotspot.txt')
    lanzar_peticiones(peticiones_hotspot, "http://127.0.0.1:80/buy/numbered")