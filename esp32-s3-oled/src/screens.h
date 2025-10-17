#ifndef SCREENS_H
#define SCREENS_H

#include <Adafruit_SSD1306.h>

// Declaración de funciones
void showSystemInfo(Adafruit_SSD1306 &display, int freeMemory);
void showGraph(Adafruit_SSD1306 &display, int freeMemory);
void showAnimation(Adafruit_SSD1306 &display);
void showClock(Adafruit_SSD1306 &display, int screen, int totalScreens);
int getFreeMemory();

#endif
