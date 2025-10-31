# ESP32 IoT Sensor - Temperatura y Humedad con MQTT y OLED

## Descripción

Este proyecto permite leer datos de un sensor de temperatura y humedad **SHT31** conectado a un **ESP32-S3** y publicarlos en un **broker MQTT** seguro (TLS). Además, los datos se muestran en tiempo real en una pantalla **OLED 128x64**.

## Requisitos

- ESP32-S3
- Sensor de temperatura y humedad SHT31
- Pantalla OLED (I2C)
- Broker MQTT con soporte TLS
- Librerías de Arduino:
  - `Adafruit_SHT31`
  - `Adafruit_SSD1306`
  - `PubSubClient`
  - `WiFiClientSecure`

## Conexiones

| Componente | Pin ESP32-S3 |
|------------|--------------|
| SCL (I2C)  | 9            |
| SDA (I2C)  | 8            |
| VCC        | 3.3V         |
| GND        | GND          |

## Configuración

Define las credenciales de Wi-Fi, MQTT y TLS en `config.h`:

```cpp
/*********** WiFi ***********/
#define WIFI_SSID "your_wifi_ssid"
#define WIFI_PASSWORD "your_wifi_password"

/*********** MQTT ***********/
#define COUNTRY "your_country"
#define STATE "your_state"
#define CITY "your_city"
#define MQTT_SERVER "your_mqtt_broker_address"
#define MQTT_PORT 8883
#define MQTT_USER "your_mqtt_username"
#define MQTT_PASSWORD "your_mqtt_password"

// Certificado raíz PEM (para TLS)
const char* ROOT_CA = R"EOF(
your_root_ca_certificate_here
)EOF";
```
