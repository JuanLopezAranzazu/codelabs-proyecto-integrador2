#include "display.h"

Display::Display(Adafruit_SSD1306* displayObj) {
  oled = displayObj;
}

bool Display::init() {
  if (!oled->begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    return false;
  }
  oled->clearDisplay();
  oled->setTextSize(1);
  oled->setTextColor(SSD1306_WHITE);
  return true;
}

void Display::showWelcome() {
  oled->clearDisplay();
  oled->setTextSize(2);
  oled->setCursor(20, 20);
  oled->println(F("ESP32-S3"));
  oled->setTextSize(1);
  oled->setCursor(15, 45);
  oled->println(F("Iniciando..."));
  oled->display();
}

void Display::showData(float temp, float hum, unsigned long uptime) {
  oled->clearDisplay();
  
  // Título
  oled->setTextSize(1);
  oled->setCursor(0, 0);
  oled->println(F("Monitor Ambiental"));
  oled->drawLine(0, 10, SCREEN_WIDTH, 10, SSD1306_WHITE);
  
  // Temperatura
  oled->setTextSize(2);
  oled->setCursor(0, 18);
  oled->print(temp, 2);
  oled->setTextSize(1);
  oled->print(" ");
  oled->print((char)247);
  oled->println("C");
  
  // Humedad
  oled->setTextSize(2);
  oled->setCursor(0, 40);
  oled->print(hum, 2);
  oled->setTextSize(1);
  oled->println(" %");
  
  oled->display();
}

void Display::showError(const char* errorMsg) {
  oled->clearDisplay();
  oled->setTextSize(1);
  oled->setCursor(0, 28);
  oled->println(errorMsg);
  oled->display();
}

void Display::clear() {
  oled->clearDisplay();
  oled->display();
}
