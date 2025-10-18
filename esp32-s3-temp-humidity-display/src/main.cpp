#include <Wire.h>
#include "config.h"
#include "display.h"
#include "sensorManager.h"

// Instancias globales
Adafruit_SSD1306 oledDisplay(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SHT31 sht31Sensor = Adafruit_SHT31();

// Objetos de gestión
Display display(&oledDisplay);
SensorManager sensorMgr(&sht31Sensor);

// Variables de control
unsigned long lastUpdate = 0;

void setup() {
  // Inicializar comunicación serial
  Serial.begin(SERIAL_BAUD);
  while (!Serial && millis() < 3000);
  
  Serial.println(F("\n=== Monitor SHT31 con OLED ==="));
  
  // Inicializar I2C
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(I2C_CLOCK);
  
  // Inicializar pantalla
  if (!display.init()) {
    Serial.println(F("ERROR: No se encontró la pantalla OLED"));
    while (1) delay(100);
  }
  Serial.println(F("Pantalla OLED inicializada"));
  
  // Inicializar sensor
  if (!sensorMgr.init()) {
    Serial.println(F("ERROR: No se encontró el sensor SHT31"));
    display.showError("Sensor Error");
    while (1) delay(100);
  }
  Serial.println(F("Sensor SHT31 inicializado"));
  
  // Mostrar pantalla de bienvenida
  display.showWelcome();
  delay(2000);
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Actualizar según intervalo definido
  if (currentMillis - lastUpdate >= UPDATE_INTERVAL) {
    lastUpdate = currentMillis;
    
    // Leer datos del sensor
    SensorData data = sensorMgr.readData();
    
    // Validar y mostrar datos
    if (data.valid) {
      display.showData(data.temperature, data.humidity, millis() / 1000);
      sensorMgr.printData(data);
    } else {
      Serial.println(F("ERROR: Lectura inválida del sensor"));
      display.showError("Lectura Error");
    }
  }
}
