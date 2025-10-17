#include "screens.h"
#include <Arduino.h>

// Función para obtener memoria libre
int getFreeMemory() {
  return ESP.getFreeHeap() / 1024; // En KB
}

// Pantalla 1: Información del sistema
void showSystemInfo(Adafruit_SSD1306 &display, int freeMemory) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println(F("=== ESP32-S3 ==="));
  display.println();
  display.print(F("CPU: "));
  display.print(ESP.getCpuFreqMHz());
  display.println(F(" MHz"));
  display.print(F("RAM: "));
  display.print(freeMemory);
  display.println(F(" KB"));
  display.println();
  display.print(F("Uptime: "));
  display.print(millis() / 1000);
  display.println(F("s"));
  display.display();
}

// Pantalla 2: Gráfico de barras
void showGraph(Adafruit_SSD1306 &display, int freeMemory) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println(F("Memoria Usada:"));
  
  int totalRAM = ESP.getHeapSize() / 1024;
  int used = totalRAM - freeMemory;
  int percentage = (used * 100) / totalRAM;
  
  // Barra de progreso
  int barWidth = map(percentage, 0, 100, 0, 128 - 10);
  display.drawRect(5, 20, 128 - 10, 15, SSD1306_WHITE);
  display.fillRect(5, 20, barWidth, 15, SSD1306_WHITE);
  
  // Porcentaje
  display.setTextSize(2);
  display.setCursor(40, 40);
  display.print(percentage);
  display.println(F("%"));
  display.display();
}

// Pantalla 3: Animación de onda
void showAnimation(Adafruit_SSD1306 &display) {
  display.clearDisplay();
  static float phase = 0;
  
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(30, 0);
  display.println(F("Onda Seno"));
  
  // Dibujar onda seno
  for (int x = 0; x < 128; x++) {
    int y = 32 + (int)(15 * sin((x + phase) * 0.1));
    display.drawPixel(x, y, SSD1306_WHITE);
  }
  
  phase += 2;
  if (phase > 360) phase = 0;

  display.display();
}

// Pantalla 4: Reloj digital
void showClock(Adafruit_SSD1306 &display, int screen, int totalScreens) {
  display.clearDisplay();
  
  unsigned long seconds = millis() / 1000;
  int hours = (seconds / 3600) % 24;
  int minutes = (seconds / 60) % 60;
  int secs = seconds % 60;
  
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(35, 0);
  display.println(F("Reloj"));
  
  display.setTextSize(2);
  display.setCursor(10, 25);
  
  if (hours < 10) display.print("0");
  display.print(hours);
  display.print(":");
  if (minutes < 10) display.print("0");
  display.print(minutes);
  display.print(":");
  if (secs < 10) display.print("0");
  display.print(secs);
  
  display.display();
}
