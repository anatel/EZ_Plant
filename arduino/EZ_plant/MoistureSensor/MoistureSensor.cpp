#include "MoistureSensor.h"

MoistureSensor::MoistureSensor() {}

MoistureSensor::MoistureSensor(const char * i_analog_pin_num)
{
  char num = i_analog_pin_num[1];

  analog_pin_num = num - '0';
}

int MoistureSensor::get_moisture_value()
{
  return analogRead(analog_pin_num);
}
