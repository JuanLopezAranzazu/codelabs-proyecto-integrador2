# Codelab Control de un LED con ESP32 a través de WiFi

## 1. ¿Qué es un ESP32 y qué características lo hacen adecuado para crear un servidor web pequeño?
El **ESP32** es un microcontrolador desarrollado por **Espressif Systems**, que incluye **WiFi y Bluetooth integrados**, además de un procesador **dual-core** y una amplia gama de **pines GPIO**.  
Sus principales características que lo hacen ideal para un servidor web pequeño son:
- Conectividad WiFi nativa.  
- Bajo consumo energético.  
- Soporte para protocolos de red (TCP/IP, HTTP, MQTT, etc.).  
- Capacidad de ejecutar múltiples tareas gracias a su arquitectura de doble núcleo.  
- Memoria suficiente para manejar peticiones y generar respuestas HTTP simples.  

Estas características permiten que el ESP32 actúe como un **servidor web embebido**, sin necesidad de un computador externo.

## 2. ¿Qué es un servidor web y cómo puede un ESP32 funcionar como uno?
Un **servidor web** es un sistema que **recibe peticiones HTTP** desde un cliente (por ejemplo, un navegador) y **responde** con información, como páginas HTML o datos.  
El ESP32 puede actuar como servidor porque:
- Abre un **puerto TCP** (en este caso, el 80).  
- Escucha las peticiones entrantes.  
- Procesa las solicitudes y genera respuestas (HTML, JSON, etc.).  

En el código, el ESP32 crea un servidor con:
```cpp
WiFiServer server(80);
```
y luego atiende a los clientes dentro del `loop()`.

## 3. ¿Cómo se utiliza la biblioteca WiFi.h en proyectos con ESP32?
La biblioteca **WiFi.h** proporciona las herramientas necesarias para:
- Conectarse a una red WiFi (`WiFi.begin()`).  
- Escanear redes disponibles (`WiFi.scanNetworks()`).  
- Obtener información de la conexión (IP, SSID, RSSI, etc.).  
- Crear y manejar servidores (`WiFiServer`) y clientes (`WiFiClient`).

En este proyecto, `WiFi.h` se usa tanto para **escanear redes disponibles** como para **conectarse** a una red y permitir la **comunicación HTTP**.

## 4. ¿Qué papel juega el protocolo HTTP en la comunicación entre un navegador web y el servidor web en el ESP32?
El **HTTP (HyperText Transfer Protocol)** define cómo los navegadores web (clientes) se comunican con los servidores web.  
En este caso:
- El **navegador** envía una petición como `GET /H` o `GET /L`.  
- El **ESP32**, como servidor, interpreta la petición y responde con una **página HTML**.  

Este protocolo es esencial para establecer una comunicación estándar entre el cliente y el servidor.

## 5. Explique el proceso de "escuchar" en un puerto específico (como el 80) en el contexto de un servidor web. ¿Por qué es importante este proceso?
Escuchar en un puerto (por ejemplo, el **puerto 80**, estándar para HTTP) significa que el servidor está **esperando conexiones entrantes** en ese canal.  
En el código:
```cpp
WiFiServer server(80);
server.begin();
```
Esto permite al ESP32 aceptar peticiones HTTP.  
Es importante porque **solo los clientes que se conecten a ese puerto** recibirán respuesta del servidor.

## 6. ¿Cómo se manejan las peticiones entrantes en un servidor web basado en ESP32? Proporcione un ejemplo de cómo se podría controlar una petición para encender un LED.
Las peticiones se manejan en el bucle principal:
```cpp
WiFiClient cliente = server.available();
```
Cuando llega una petición, el ESP32 analiza el texto recibido.  
Si detecta:
```cpp
mensaje.endsWith("GET /H")
```
enciende el LED con `digitalWrite(2, HIGH);`.  
Si detecta:
```cpp
mensaje.endsWith("GET /L")
```
lo apaga con `digitalWrite(2, LOW);`.  

De esta forma, el ESP32 interpreta comandos HTTP simples para controlar hardware.

## 7. ¿Qué es una dirección IP local y cómo se asigna al ESP32 cuando se conecta a una red WiFi? ¿Por qué es importante para acceder al servidor web?
La **IP local** identifica al ESP32 dentro de la red WiFi.  
Se obtiene con:
```cpp
WiFi.localIP();
```
El router la asigna mediante **DHCP** al conectarse.  
Es esencial porque esta dirección permite que el navegador acceda al servidor web, escribiendo en la barra de direcciones algo como:
```
http://192.168.1.105
```

## 8. Explique la diferencia entre una conexión WiFi abierta y una segura. ¿Cómo afecta esto a un proyecto que involucra un ESP32 actuando como servidor web?
- **Red abierta:** no requiere contraseña (menos segura).  
- **Red segura:** usa cifrado (WEP, WPA, WPA2, etc.).  

En un proyecto con ESP32, usar una red segura es fundamental para **evitar accesos no autorizados**, especialmente si el servidor controla hardware sensible o expone datos.

## 9. ¿Cuáles son los desafíos de seguridad que deben considerarse cuando se expone un ESP32 a una red como servidor web y cómo se pueden mitigar?
**Desafíos:**
- Acceso no autorizado desde la red.  
- Transmisión de datos sin cifrar (HTTP).  
- Posibles ataques DoS o sniffing.  

**Medidas de mitigación:**
- Usar **redes WPA2** o superiores.  
- Implementar **autenticación por contraseña** en el servidor web.  
- Evitar exponer el dispositivo directamente a Internet.  
- Usar **HTTPS** si es posible.

## 10. ¿Cómo se utiliza la función WiFiClient para manejar clientes web en el ESP32? Describa el ciclo de vida de una conexión desde que el cliente se conecta hasta que se cierra la conexión.
`WiFiClient` representa al **cliente web** que se conecta al servidor.  
El ciclo es:
1. **Conexión:** `server.available()` detecta un nuevo cliente.  
2. **Lectura:** se leen los datos de la petición (`cliente.read()`).  
3. **Procesamiento:** se analiza la petición (por ejemplo, `/H` o `/L`).  
4. **Respuesta:** el ESP32 envía HTML al navegador (`cliente.println()`).  
5. **Cierre:** se termina la conexión con `cliente.stop()`.

## 11. ¿Cómo se inicializa el servidor web en el ESP32 y en qué puerto escucha por defecto según el código proporcionado?
En el código:
```cpp
WiFiServer server(80);
server.begin();
```
Esto inicia un **servidor HTTP** que escucha en el **puerto 80**, el puerto predeterminado para tráfico web.

## 12. Analiza cómo se crea una instancia del WiFiServer y se le asigna un puerto para escuchar las conexiones entrantes.
```cpp
WiFiServer server(80);
```
Crea una instancia del servidor y le asigna el puerto **80** para escuchar peticiones.  
Solo las conexiones dirigidas a este puerto serán atendidas.

## 13. Explique el propósito de la función scanNetworks() en el código y qué información específica se imprime sobre las redes WiFi disponibles.
La función:
```cpp
WiFi.scanNetworks();
```
busca todas las redes WiFi disponibles y devuelve su número.  
Luego imprime información como:
- Nombre (SSID)  
- Intensidad de señal (RSSI)  
- Dirección MAC  
- Tipo de cifrado  

Esto permite al usuario **diagnosticar la calidad de la señal** o **elegir la red adecuada** para conectar el ESP32.

## 14. Considera qué datos se recopilan durante el escaneo de redes y cómo esto podría ser útil para el diagnóstico o la configuración de la conexión WiFi.
Se obtienen:
- SSID (nombre de la red).  
- Nivel de señal (dBm).  
- MAC del punto de acceso.  
- Tipo de cifrado.  

Estos datos son útiles para configurar la conexión o detectar redes inseguras o congestionadas.

## 15. Describa cómo se establece la conexión WiFi en el código. ¿Qué sucede si la conexión no se puede establecer de inmediato?
En el código:
```cpp
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.print(".");
}
```
El ESP32 intenta conectarse repetidamente hasta que obtiene conexión.  
Si la conexión falla, el bucle sigue intentando cada segundo.

## 16. Examina el bucle que espera a que el ESP32 se conecte a la red WiFi y cómo se manejan los intentos repetidos de conexión.
El bucle `while` controla los intentos de conexión:
```cpp
while (WiFi.status() != WL_CONNECTED)
```
Esto garantiza que el código **no avance** hasta lograr la conexión.  
Se imprime un punto cada segundo para indicar progreso al usuario.

## 17. Analice cómo se manejan las peticiones HTTP entrantes en el bucle principal (loop) y cómo se determina la acción a realizar (por ejemplo, encender o apagar un LED).
Dentro de `loop()`, el código:
- Espera clientes (`server.available()`).  
- Lee las peticiones (`cliente.read()`).  
- Interpreta comandos (`GET /H` o `GET /L`).  

Dependiendo del comando, ejecuta acciones (encender/apagar LED).  
Esto demuestra cómo un servidor web embebido puede **controlar hardware físico** mediante peticiones HTTP.

## 18. Observa cómo se lee y procesa la petición del cliente para ejecutar acciones específicas basadas en la URL solicitada.
El ESP32 va leyendo cada carácter de la petición y la almacena en una cadena (`mensaje`).  
Cuando detecta que termina la línea (`\n`), analiza el contenido.  
Si detecta comandos específicos (`GET /H`, `GET /L`), ejecuta la acción correspondiente.

## 19. ¿Cómo se envía la respuesta HTTP al cliente desde el ESP32, y qué contenido se incluye en esa respuesta según el ejemplo del código?
Una vez interpretada la petición, el ESP32 envía:
```cpp
cliente.println("HTTP/1.1 200 OK");
cliente.println("Content-type:text/html");
cliente.println();
cliente.println("<br>Clic <a href=\"H\">aqui</a> para encender la lampara<br>");
cliente.println("Clic <a href=\"L\">aqui</a> para apagar la lampara");
cliente.println();
```
Esto incluye los **encabezados HTTP** y el **contenido HTML** que el navegador mostrará.

## 20. Considera la estructura de la respuesta HTTP generada por el ESP32, incluyendo los encabezados y el cuerpo de la respuesta, y cómo se comunica el estado del LED o se proporcionan instrucciones al usuario.
La respuesta tiene:
1. **Línea de estado:** `HTTP/1.1 200 OK` → indica que la petición fue exitosa.  
2. **Encabezados:** `Content-type:text/html` → especifica el tipo de contenido.  
3. **Cuerpo HTML:** contiene los enlaces para encender o apagar la lámpara.  

El navegador interpreta esta respuesta y muestra una página con dos enlaces interactivos.

## Requisitos

- Placa ESP32.
- Entorno de desarrollo PlatformIO con VSCode.
- Acceso a una red WiFi.

## Compilar y subir el programa

1. Conecta tu ESP32-S3 al puerto USB.
2. Haz clic en Build (compilar) en PlatformIO.
3. Haz clic en Upload (subir) para cargar el programa en la placa.
4. Presiona RESET si el monitor serie se queda esperando.

## Uso

1. Abrir el Monitor Serie en VSCode.
2. Esperar a que la ESP32 se conecte al WiFi y muestre la IP
3. Abrir un navegador en la misma red WiFi y acceder a la IP mostrada
