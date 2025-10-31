#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_SHT31.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include "config.h"

// ==================== Objetos ====================
Adafruit_SHT31 sht31 = Adafruit_SHT31();
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
WiFiClientSecure espClient;
PubSubClient client(espClient);

// ==================== Variables globales ====================
unsigned long lastMeasure = 0;
String macAddress;
String clientId;
String topicPublish;
String topicSubscribe;

// ==================== Funciones auxiliares ====================

/**
 * Inicializa la pantalla OLED
 * @return true si la inicialización fue exitosa
 */
bool initDisplay() {
    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
        Serial.println(F("Error: No se pudo inicializar la pantalla OLED"));
        return false;
    }
    
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println(F("Iniciando..."));
    display.display();
    
    Serial.println(F("Pantalla OLED inicializada"));
    return true;
}

/**
 * Inicializa el sensor de temperatura y humedad
 * @return true si la inicialización fue exitosa
 */
bool initSensor() {
    if (!sht31.begin(SHT31_ADDR)) {
        Serial.println(F("Error: No se pudo inicializar el sensor SHT31"));
        return false;
    }
    
    Serial.println(F("Sensor SHT31 inicializado"));
    return true;
}

/**
 * Conecta a la red WiFi
 * @return true si la conexión fue exitosa
 */
bool connectWiFi() {
    Serial.print(F("Conectando a WiFi: "));
    Serial.println(WIFI_SSID);
    
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    uint8_t attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < WIFI_TIMEOUT) {
        delay(1000);
        Serial.print(F("."));
        attempts++;
    }
    
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println(F("\nError: No se pudo conectar a WiFi"));
        return false;
    }
    
    Serial.println(F("\nWiFi conectado"));
    Serial.print(F("IP: "));
    Serial.println(WiFi.localIP());
    Serial.print(F("RSSI: "));
    Serial.print(WiFi.RSSI());
    Serial.println(F(" dBm"));
    
    return true;
}

/**
 * Configura los tópicos MQTT dinámicos
 */
void setupMqttTopics() {
    // Obtener MAC address para usar como client ID
    macAddress = WiFi.macAddress();
    clientId = macAddress;
    
    // Tópicos dinámicos
    topicPublish = String(COUNTRY) + "/" + String(STATE) + "/" + String(CITY) + "/" + 
                   clientId + "/" + String(MQTT_USER) + "/out";
    
    topicSubscribe = String(COUNTRY) + "/" + String(STATE) + "/" + String(CITY) + "/" + 
                     clientId + "/" + String(MQTT_USER) + "/in";
    
    Serial.println(F("\n--- Configuración MQTT ---"));
    Serial.print(F("Client ID: "));
    Serial.println(clientId);
    Serial.print(F("Publicar: "));
    Serial.println(topicPublish);
    Serial.print(F("Suscribir: "));
    Serial.println(topicSubscribe);
}

/**
 * Callback para mensajes MQTT recibidos
 */
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    Serial.print(F("Mensaje recibido ["));
    Serial.print(topic);
    Serial.print(F("]: "));
    
    for (unsigned int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}

/**
 * Reconecta al broker MQTT
 */
void reconnectMqtt() {
    while (!client.connected()) {
        Serial.print(F("Conectando a MQTT broker..."));
        
        if (client.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
            Serial.println(F(" Conectado"));
            
            // Suscribirse al tópico
            if (client.subscribe(topicSubscribe.c_str())) {
                Serial.print(F("Suscrito a: "));
                Serial.println(topicSubscribe);
            } else {
                Serial.println(F("Error en suscripción"));
            }
        } else {
            Serial.print(F("Falló, rc="));
            Serial.print(client.state());
            Serial.print(F(" - Reintentando en "));
            Serial.print(MQTT_RETRY_DELAY);
            Serial.println(F(" segundos"));
            
            delay(MQTT_RETRY_DELAY * 1000);
        }
    }
}

/**
 * Muestra información en la pantalla OLED
 */
void displayInfo(float temp, float hum, bool sensorError = false) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(1);
    
    if (sensorError) {
        display.println(F("ERROR SENSOR"));
        display.println(F("Verificar conexion"));
    } else {
        display.setTextSize(1);
        display.println(F("Temperatura:"));
        display.setTextSize(2);
        display.printf("%.2f C\n", temp);
        
        display.setTextSize(1);
        display.println(F("Humedad:"));
        display.setTextSize(2);
        display.printf("%.2f %%", hum);
    }
    
    display.display();
}

/**
 * Lee y publica datos del sensor
 */
void readAndPublishSensorData() {
    float temp = sht31.readTemperature();
    float hum = sht31.readHumidity();
    
    // Validar lecturas
    if (isnan(temp) || isnan(hum)) {
        Serial.println(F("Error: Lectura inválida del sensor"));
        displayInfo(0, 0, true);
        return;
    }
    
    // Crear payload JSON
    char payload[PAYLOAD_BUFFER_SIZE];
    snprintf(payload, PAYLOAD_BUFFER_SIZE,
             "{\"temperatura\":%.2f,\"humedad\":%.2f}",
             temp, hum);
    
    // Publicar con retain flag
    bool published = client.publish(topicPublish.c_str(), payload, true);
    
    if (published) {
        Serial.println(F("Datos publicados"));
        Serial.print(F("  Temperatura: "));
        Serial.print(temp, 2);
        Serial.println(F(" °C"));
        Serial.print(F("  Humedad: "));
        Serial.print(hum, 2);
        Serial.println(F(" %"));
    } else {
        Serial.println(F("Error al publicar"));
    }
    
    // Actualizar display
    displayInfo(temp, hum);
}

// ==================== Setup ====================
void setup() {
    // Inicializar serial
    Serial.begin(SERIAL_BAUD);
    delay(1000);
    Serial.println(F("\n\n=== Monitor de Temperatura y Humedad ===\n"));
    
    // Inicializar I2C
    Wire.begin(SDA_PIN, SCL_PIN, I2C_CLOCK);
    Serial.println(F("Bus I2C inicializado"));
    
    // Inicializar periféricos
    if (!initDisplay()) {
        while (1) delay(1000);
    }
    
    if (!initSensor()) {
        display.clearDisplay();
        display.setCursor(0, 0);
        display.println(F("Error Sensor"));
        display.display();
        while (1) delay(1000);
    }
    
    // Conectar WiFi
    if (!connectWiFi()) {
        display.clearDisplay();
        display.setCursor(0, 0);
        display.println(F("Error WiFi"));
        display.display();
        while (1) delay(1000);
    }
    
    // Configurar MQTT
    setupMqttTopics();
    espClient.setCACert(ROOT_CA);
    client.setServer(MQTT_SERVER, MQTT_PORT);
    client.setCallback(mqttCallback);
    client.setBufferSize(512);
    
    Serial.println(F("\nSistema inicializado correctamente\n"));
    
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println(F("Sistema OK"));
    display.display();
    delay(2000);
}

// ==================== Loop ====================
void loop() {
    // Verificar conexión MQTT
    if (!client.connected()) {
        reconnectMqtt();
    }
    client.loop();
    
    // Leer y publicar datos periódicamente
    unsigned long now = millis();
    if (now - lastMeasure >= UPDATE_INTERVAL) {
        lastMeasure = now;
        readAndPublishSensorData();
    }
    
    // Verificar conexión WiFi
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println(F("WiFi desconectado, reconectando..."));
        connectWiFi();
    }
}
