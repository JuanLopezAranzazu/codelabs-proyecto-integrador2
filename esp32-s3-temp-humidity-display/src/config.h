#ifndef CONFIG_H
#define CONFIG_H

// Configuración de pines I2C
#define SDA_PIN 8
#define SCL_PIN 9

// Configuración de pantalla
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C

// Configuración del sensor
#define SHT31_ADDR 0x44
#define UPDATE_INTERVAL 5000  // ms

// Configuración serial
#define SERIAL_BAUD 115200
#define I2C_CLOCK 400000  // Hz

#endif
