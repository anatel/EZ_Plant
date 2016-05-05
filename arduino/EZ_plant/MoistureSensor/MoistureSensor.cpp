#include "MoistureSensor.h"

MoistureSensor::MoistureSensor() {}

MoistureSensor::MoistureSensor(int i_analog_pin_num)
{
  analog_pin_num = i_analog_pin_num;
}

int MoistureSensor::get_moisture_value()
{
  return analogRead(analog_pin_num);
}
