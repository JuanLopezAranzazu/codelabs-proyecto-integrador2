#ifndef CONFIG_H
#define CONFIG_H

/*********** Pines y periféricos ***********/
#define SDA_PIN 8
#define SCL_PIN 9

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C

#define SHT31_ADDR 0x44
#define UPDATE_INTERVAL 5000  // ms

#define SERIAL_BAUD 115200
#define I2C_CLOCK 400000  // Hz

/*********** WiFi ***********/
#define WIFI_SSID "your_wifi_ssid"
#define WIFI_PASSWORD "your_wifi_password"
#define WIFI_TIMEOUT 30     // segundos

/*********** MQTT ***********/
#define COUNTRY "your_country"
#define STATE "your_state"
#define CITY "your_city"
#define MQTT_SERVER "your_mqtt_broker_address"
#define MQTT_PORT 8883
#define MQTT_USER "your_mqtt_username"
#define MQTT_PASSWORD "your_mqtt_password"

#define MQTT_RETRY_DELAY 5  // segundos
#define TOPIC_BUFFER_SIZE 128
#define PAYLOAD_BUFFER_SIZE 256

// Certificado raíz PEM (para TLS)
const char* ROOT_CA = R"EOF(
your_root_ca_certificate_here
)EOF";

#endif
