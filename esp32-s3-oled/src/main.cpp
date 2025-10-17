#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "screens.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define SDA_PIN 8
#define SCL_PIN 9
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Variables globales
unsigned long previousTime = 0;
int currentScreen = 0;
const int totalScreens = 4;
int freeMemory = 0;

void setup() {
  Serial.begin(115200);
  delay(100);
  
  Serial.println(F("\n=== Sistema OLED con ESP32-S3 ==="));
  
  // Inicializar I2C
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(400000); // I2C a 400kHz para mayor velocidad
  
  // Inicializar display
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("ERROR: No se pudo inicializar el SSD1306"));
    Serial.println(F("Verifique las conexiones:"));
    Serial.println(F("- SDA -> Pin 8"));
    Serial.println(F("- SCL -> Pin 9"));
    Serial.println(F("- VCC -> 3.3V"));
    Serial.println(F("- GND -> GND"));
    while(1) delay(1000);
  }
  
  Serial.println(F("SSD1306 inicializado correctamente"));
  
  // Pantalla de bienvenida
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(10, 5);
  display.println(F("ESP32-S3"));
  display.setTextSize(1);
  display.setCursor(15, 30);
  display.println(F("Sistema OLED"));
  display.display();
  delay(3000);
}

void loop() {
  unsigned long currentTime = millis();
  
  // Cambiar de pantalla cada 3 segundos
  if (currentTime - previousTime >= 3000) {
    previousTime = currentTime;
    currentScreen = (currentScreen + 1) % totalScreens;
    
    // Actualizar datos
    freeMemory = getFreeMemory();
    
    Serial.print(F("Pantalla: "));
    Serial.print(currentScreen + 1);
    Serial.print(F(" | RAM: "));
    Serial.print(freeMemory);
    Serial.println(F(" KB"));
  }
  
  // Mostrar pantalla actual
  switch(currentScreen) {
    case 0:
      showSystemInfo(display, freeMemory);
      break;
    case 1:
      showGraph(display, freeMemory);
      break;
    case 2:
      showAnimation(display);
      break;
    case 3:
      showClock(display, currentScreen, totalScreens);
      break;
  }
  
  delay(50); // Actualización suave
}
