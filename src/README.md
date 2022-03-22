# Directorios

- **DBSuscriptor:** Un script en python el cual se suscribe a todos los mensajes del Broker HiveMQ (MQTT), para posteriormente enviarlos a la base de datos de InfluxDB.
- **MatLab Script:** Script elaborado en MatLab, hecho por *Tom Irvine (tom@vibrationdata.com*), el cual permite convertir la aceleración temporal por una aceleración ponderada según el ISO 2631. Además, también realiza algunas tareas de filtrado de datos.
- **OLD:** Contiene una versión que al final no se usaron, para poder administrar, controlar y monitorizar las Raspberries PI y sus sensores. Este se instalaba dentro de la Raspberry, y consistía en una interfaz web almacenada en la Raspberry y que se podia acceder a través de su IP. Sin embargo, **no se llegó a implementar**.
- **PanelBB:** Front End que permite visualizar los datos de los sensores en tiempo real. **Nunca se llegó a implementar finalmente**.
- **PanelBroker:** Implementación de un panel Front End para poder comprobar los datos que llegan desde los sensores hacia el broker. **Nunca se llegó a implementar finalmente.**
- **Raspberry PI:** Contiene el software necesario para la obtención de datos de los sensores desde la Raspberry PI, y su envío al broker. Hay varias versiones, ya que se modificó para la toma de datos para calcular el índice del mareo. Dentro del directorio hay más información.