import pika
import redis
import json
import time
import sys

db = redis.Redis(host='localhost', port=6379, decode_responses=True)

def procesar_logica_negocio(nombre_cola, peticion, exitos, fallos):
    if nombre_cola == 'cola_unnumbered':
        quedan = db.decr('tickets_disponibles')
        if quedan >= 0:
            return exitos + 1, fallos
        else:
            db.incr('tickets_disponibles')
            return exitos, fallos + 1
    else:
        clave_asiento = f"asiento:{peticion['seat_id']}"
        comprado = db.setnx(clave_asiento, peticion['client_id'])
        if comprado:
            return exitos + 1, fallos
        else:
            return exitos, fallos + 1

def iniciar_worker_automatico():
    conexion = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conexion.channel()
    
    colas = ['cola_unnumbered', 'cola_numbered', 'cola_hotspot']
    for c in colas:
        canal.queue_declare(queue=c)

    canal.basic_qos(prefetch_count=1000)

    print("🤖 Worker Automático Iniciado (Versión Turbo 🚀).")
    print("👀 Vigilando las 3 colas. Pulsa CTRL+C para salir.\n")

    while True:
        for nombre_cola in colas:
            estado_cola = canal.queue_declare(queue=nombre_cola, passive=True)
            mensajes_esperando = estado_cola.method.message_count
            
            if mensajes_esperando > 0:
                print(f"\n🚀 ¡Avalancha de {mensajes_esperando} mensajes en '{nombre_cola}'!")
                
                db.flushdb()
                db.set('tickets_disponibles', 20000)
                print("🧹 Base de datos reseteada automáticamente.")
                
                procesados, exitos, fallos = 0, 0, 0
                inicio_tiempo = time.time() # <-- Empezamos el cronómetro
                
                for method, properties, body in canal.consume(queue=nombre_cola, inactivity_timeout=1):
                    if method is None:
                        break
                        
                    peticion = json.loads(body)
                    exitos, fallos = procesar_logica_negocio(nombre_cola, peticion, exitos, fallos)
                    canal.basic_ack(delivery_tag=method.delivery_tag)
                    procesados += 1
                    
                    if procesados % 5000 == 0:
                        print(f"⚙️ Procesados: {procesados}...")

                canal.cancel()
                
                # --- ARREGLO DEL CRONÓMETRO ---
                tiempo_final = time.time()
                duracion = (tiempo_final - 1) - inicio_tiempo # Restamos 1 seg del timeout
                if duracion <= 0: duracion = 0.01 # Evitamos divisiones por cero por seguridad
                
                print(f"✅ TEST COMPLETADO: {nombre_cola}")
                print(f"📊 Éxitos: {exitos} | Fallos: {fallos}")
                print(f"⏱️ Tiempo: {duracion:.2f} s")
                print(f"⚡ Rendimiento: {procesados / duracion:.2f} pet/seg")
                print("-" * 40)
                
        time.sleep(1)

if __name__ == '__main__':
    try:
        iniciar_worker_automatico()
    except KeyboardInterrupt:
        print("\nApagando worker...")
        sys.exit(0)