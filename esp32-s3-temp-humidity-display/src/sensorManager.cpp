#include "sensorManager.h"

SensorManager::SensorManager(Adafruit_SHT31* sensorObj) {
  sensor = sensorObj;
}

bool SensorManager::init() {
  return sensor->begin(SHT31_ADDR);
}

SensorData SensorManager::readData() {
  SensorData data;
  data.temperature = sensor->readTemperature();
  data.humidity = sensor->readHumidity();
  data.valid = !isnan(data.temperature) && !isnan(data.humidity);
  return data;
}

void SensorManager::printData(const SensorData& data) {
  if (!data.valid) {
    Serial.println(F("ERROR: Lectura inválida"));
    return;
  }
  
  Serial.print(F("Temperatura: "));
  Serial.print(data.temperature, 2);
  Serial.print(F(" °C | Humedad: "));
  Serial.print(data.humidity, 2);
  Serial.println(F(" %"));
}
