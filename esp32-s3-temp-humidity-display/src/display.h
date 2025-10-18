#ifndef DISPLAY_H
#define DISPLAY_H

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "config.h"

class Display {
private:
  Adafruit_SSD1306* oled;
  
public:
  Display(Adafruit_SSD1306* displayObj);
  bool init();
  void showWelcome();
  void showData(float temp, float hum, unsigned long uptime);
  void showError(const char* errorMsg);
  void clear();
};

#endif
