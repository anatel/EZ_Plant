#ifndef MoistureSensor_h
#define MoistureSensor_h

#include "Arduino.h"
#include <SPI.h>

class MoistureSensor
{
  private:
    int analog_pin_num;

  public:
    MoistureSensor();
    MoistureSensor(int i_analog_pin_num);
    int get_moisture_value();
};

#endif
