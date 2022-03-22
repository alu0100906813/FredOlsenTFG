# Descripción

Encontramos dos versiones del main:

- **main.py:** Versión modificada para obtener datos desde una Raspberry PI, y poder almacenarlos en una base de datos interna, para posteriormente extraerlos y calcular el índice de mareo. También se incluye el fichero *mysql.py*, para realizar la conexión e inserción en la base de datos.
- **main_original.py:** Contiene la versión original que envía datos mediante el protocolo MQTT hacía el broker, y este hacia la base de datos.