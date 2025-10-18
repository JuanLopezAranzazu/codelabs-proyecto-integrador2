#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include <Adafruit_SHT31.h>
#include "config.h"

struct SensorData {
  float temperature;
  float humidity;
  bool valid;
};

class SensorManager {
private:
  Adafruit_SHT31* sensor;
  
public:
  SensorManager(Adafruit_SHT31* sensorObj);
  bool init();
  SensorData readData();
  void printData(const SensorData& data);
};

#endif
