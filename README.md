ESTO CON 1 UNICO WORKER
PS C:\Users\paupl\OneDrive\Desktop\UNI\3r Curs\2n quatri\SD\SD_practica1> python client.py
🧹 Base de datos limpiada.
=== TEST 1: ENTRADAS NO NUMERADAS ===
🚀 Iniciando envío de 20000 peticiones a http://127.0.0.1:8000/buy/unnumbered...

--- 📊 RESULTADOS ---
✅ Compras exitosas: 20000
❌ Compras fallidas (rechazadas por BD): 0
⏱️ Tiempo total: 45.40 segundos
⚡ Rendimiento: 440.51 pet/seg

=== TEST 2: ENTRADAS NUMERADAS ===
🧹 Base de datos limpiada.
🚀 Iniciando envío de 25997 peticiones a http://127.0.0.1:8000/buy/numbered...

--- 📊 RESULTADOS ---
✅ Compras exitosas: 20000
❌ Compras fallidas (rechazadas por BD): 5997
⏱️ Tiempo total: 57.31 segundos
⚡ Rendimiento: 453.60 pet/seg

CON 3 WORKERS
🧹 Base de datos limpiada.
=== TEST 1: ENTRADAS NO NUMERADAS ===
🚀 Iniciando envío de 20000 peticiones a http://127.0.0.1:80/buy/unnumbered...

--- 📊 RESULTADOS ---
✅ Compras exitosas: 20000
❌ Compras fallidas (rechazadas por BD): 0
⏱️ Tiempo total: 38.56 segundos
⚡ Rendimiento: 518.61 pet/seg

=== TEST 2: ENTRADAS NUMERADAS ===
🧹 Base de datos limpiada.
🚀 Iniciando envío de 25997 peticiones a http://127.0.0.1:80/buy/numbered...

--- 📊 RESULTADOS ---
✅ Compras exitosas: 20000
❌ Compras fallidas (rechazadas por BD): 5997
⏱️ Tiempo total: 45.63 segundos
⚡ Rendimiento: 569.69 pet/seg

PORQUE AL PASAR DE 1 WORKER A 3 NO MEJORAMOS X3 EL RENDIMIENTO?
La respuesta es por el client.py, es un cuello de botella, envia las peticiones de 1 en 1 dentro de un bucle for,
no estresamos al worker al 100%

ATAQUE DE HOTSPOT:
PS C:\Users\paupl\OneDrive\Desktop\UNI\3r Curs\2n quatri\SD\SD_practica1> python .\generador_hotspot.py
🔥 Generando archivo de Alta Contención...
📊 Resumen de la generación:
 - Total peticiones: 25997
 - Peticiones al Hotspot (1-1000): 20833 (80.1%)
✅ Archivo 'benchmark_hotspot.txt' creado con éxito.

PS C:\Users\paupl\OneDrive\Desktop\UNI\3r Curs\2n quatri\SD\SD_practica1> python client.py
🧹 Base de datos limpiada.
=== TEST 1: ENTRADAS NO NUMERADAS ===
🚀 Iniciando envío de 20000 peticiones a http://127.0.0.1:80/buy/unnumbered...

--- 📊 RESULTADOS ---
✅ Compras exitosas: 20000
❌ Compras fallidas (rechazadas por BD): 0
⏱️ Tiempo total: 41.01 segundos
⚡ Rendimiento: 487.63 pet/seg

=== TEST 2: ENTRADAS NUMERADAS ===
🧹 Base de datos limpiada.
🚀 Iniciando envío de 25997 peticiones a http://127.0.0.1:80/buy/numbered...

--- 📊 RESULTADOS ---
✅ Compras exitosas: 20000
❌ Compras fallidas (rechazadas por BD): 5997
⏱️ Tiempo total: 56.41 segundos
⚡ Rendimiento: 460.86 pet/seg

=== TEST 3: ENTRADAS NUMERADAS (HOTSPOT) 🔥 ===
🧹 Base de datos limpiada.
🚀 Iniciando envío de 25997 peticiones a http://127.0.0.1:80/buy/numbered...

--- 📊 RESULTADOS ---
✅ Compras exitosas: 5518
❌ Compras fallidas (rechazadas por BD): 20479
⏱️ Tiempo total: 51.56 segundos
⚡ Rendimiento: 504.23 pet/seg

SUBIDA NOTABLE DE RENDIMIENTO Y DE COMPRAS FALLIDAS, TOTALMENTE NORMAL AL INTENTAR COMPRAR EL MISMO ASIENTO YA QUE REDDIS DEVUELVE
0 AL YA ESTAR OCUPADA PRACTICAMENTE AL INSTANTE PROCESANDO MAS DATOS POR SEGUNDO


USANDO RABBIT
PS C:\Users\paupl\OneDrive\Desktop\UNI\3r Curs\2n quatri\SD\SD_practica1> python .\productor.py
=== TEST INDIRECTO: ENTRADAS NO NUMERADAS ===
🚀 Enviando 20000 mensajes a la cola 'cola_unnumbered'...

--- 📊 RESULTADOS DEL PRODUCTOR ---
✅ Mensajes encolados: 20000
⏱️ Tiempo en encolar: 0.73 segundos
⚡ Velocidad de encolado: 27241.36 msg/seg

RENDIMIENTO PURO
En REST: El cliente espera a que el Worker vaya a Redis, haga el cálculo, y le devuelva una respuesta por la red. Es síncrono y lento.

En RabbitMQ: El cliente suelta el mensaje en la RAM de RabbitMQ y se desentiende. Es asíncrono y ridículamente rápido.
PS C:\Users\paupl\OneDrive\Desktop\UNI\3r Curs\2n quatri\SD\SD_practica1> python .\consumer.py
🧹 Base de datos reseteada a 20.000 entradas.
 [*] Esperando mensajes en 'cola_unnumbered'...
⏳ Empezando a procesar la avalancha de mensajes...

--- 📊 RESULTADOS DEL CONSUMIDOR ---
✅ Entradas procesadas en Redis: 20000
⏱️ Tiempo de procesamiento: 10.36 segundos
⚡ Rendimiento: 1929.71 pet/seg

UN AUMENTO NOTABLE DE RENDIMIENTO


PS C:\Users\paupl\OneDrive\Desktop\UNI\3r Curs\2n quatri\SD\SD_practica1> python .\consumer.py
🤖 Worker Automático Iniciado (Versión Turbo 🚀).
👀 Vigilando las 3 colas. Pulsa CTRL+C para salir.


🚀 ¡Avalancha de 34903 mensajes en 'cola_unnumbered'!
🧹 Base de datos reseteada automáticamente.
⚙️ Procesados: 5000...
⚙️ Procesados: 10000...
⚙️ Procesados: 15000...
⚙️ Procesados: 20000...
⚙️ Procesados: 25000...
⚙️ Procesados: 30000...
✅ TEST COMPLETADO: cola_unnumbered
📊 Éxitos: 20000 | Fallos: 14903
⏱️ Tiempo: 1774554418.11 s
⚡ Rendimiento: 0.00 pet/seg
----------------------------------------

🚀 ¡Avalancha de 77896 mensajes en 'cola_numbered'!
🧹 Base de datos reseteada automáticamente.
⚙️ Procesados: 5000...
⚙️ Procesados: 10000...
⚙️ Procesados: 15000...
⚙️ Procesados: 20000...
⚙️ Procesados: 25000...
⚙️ Procesados: 30000...
⚙️ Procesados: 35000...
⚙️ Procesados: 40000...
⚙️ Procesados: 45000...
⚙️ Procesados: 50000...
⚙️ Procesados: 55000...
⚙️ Procesados: 60000...
⚙️ Procesados: 65000...
⚙️ Procesados: 70000...
⚙️ Procesados: 75000...
✅ TEST COMPLETADO: cola_numbered
📊 Éxitos: 20000 | Fallos: 57896
⏱️ Tiempo: 1774554460.32 s
⚡ Rendimiento: 0.00 pet/seg
----------------------------------------

🚀 ¡Avalancha de 77991 mensajes en 'cola_hotspot'!
🧹 Base de datos reseteada automáticamente.
⚙️ Procesados: 5000...
⚙️ Procesados: 10000...
⚙️ Procesados: 15000...
⚙️ Procesados: 20000...
⚙️ Procesados: 25000...
⚙️ Procesados: 30000...
⚙️ Procesados: 35000...
⚙️ Procesados: 40000...
⚙️ Procesados: 45000...
⚙️ Procesados: 50000...
⚙️ Procesados: 55000...
⚙️ Procesados: 60000...
⚙️ Procesados: 65000...
⚙️ Procesados: 70000...
⚙️ Procesados: 75000...
✅ TEST COMPLETADO: cola_hotspot
📊 Éxitos: 5518 | Fallos: 72473
⏱️ Tiempo: 1774554503.59 s
⚡ Rendimiento: 0.00 pet/seg
----------------------------------------

TEMPORIZADOR Y RENDIMIENTO ARREGLADOS
PS C:\Users\paupl\OneDrive\Desktop\UNI\3r Curs\2n quatri\SD\SD_practica1> python .\consumer.py
🤖 Worker Automático Iniciado (Versión Turbo 🚀).
👀 Vigilando las 3 colas. Pulsa CTRL+C para salir.


🚀 ¡Avalancha de 16386 mensajes en 'cola_unnumbered'!
🧹 Base de datos reseteada automáticamente.
⚙️ Procesados: 5000...
⚙️ Procesados: 10000...
⚙️ Procesados: 15000...
⚙️ Procesados: 20000...
✅ TEST COMPLETADO: cola_unnumbered
📊 Éxitos: 20000 | Fallos: 0
⏱️ Tiempo: 12.13 s
⚡ Rendimiento: 1648.61 pet/seg
----------------------------------------

🚀 ¡Avalancha de 25997 mensajes en 'cola_numbered'!
🧹 Base de datos reseteada automáticamente.
⚙️ Procesados: 5000...
⚙️ Procesados: 10000...
⚙️ Procesados: 15000...
⚙️ Procesados: 20000...
⚙️ Procesados: 25000...
✅ TEST COMPLETADO: cola_numbered
📊 Éxitos: 20000 | Fallos: 5997
⏱️ Tiempo: 13.93 s
⚡ Rendimiento: 1865.94 pet/seg
----------------------------------------

🚀 ¡Avalancha de 25997 mensajes en 'cola_hotspot'!
🧹 Base de datos reseteada automáticamente.
⚙️ Procesados: 5000...
⚙️ Procesados: 10000...
⚙️ Procesados: 15000...
⚙️ Procesados: 20000...
⚙️ Procesados: 25000...
✅ TEST COMPLETADO: cola_hotspot
📊 Éxitos: 5518 | Fallos: 20479
⏱️ Tiempo: 13.59 s
⚡ Rendimiento: 1913.14 pet/seg
----------------------------------------

