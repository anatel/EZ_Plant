#include "WaterPump.h"

WaterPump::WaterPump() {}

WaterPump::WaterPump(int i_digital_pin_num)
{
  digital_pin_num = i_digital_pin_num;
  pinMode(digital_pin_num, OUTPUT);
  digitalWrite(digital_pin_num, HIGH);
}

void WaterPump::start_pumping()
{
  digitalWrite(digital_pin_num, LOW);
}

void WaterPump::stop_pumping()
{
  digitalWrite(digital_pin_num, HIGH);
}
