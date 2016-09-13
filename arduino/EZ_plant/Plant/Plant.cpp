#include "Plant.h"

Plant::Plant() {}

Plant::Plant(const char * i_plant_id, const char * sensor_pin_num, int water_pump_pin_num)
{
  plant_id = i_plant_id;
  being_watered_now = false;
  moisture_sensor = MoistureSensor(sensor_pin_num);
  water_pump = WaterPump(water_pump_pin_num);
  low_threshold = 100;
}

int Plant::get_current_moisture_value()
{
  return current_moisture_value;
}

bool Plant::is_low_threshold_legal(int threshold)
{
  return (threshold >= 203 && threshold <= 1024);
}

bool Plant::is_it_time_to_water()
{
  update_current_moisture_value();
  if (is_low_threshold_legal(low_threshold))
  {
    return current_moisture_value >= low_threshold;
  }

  return false;
}

void Plant::set_low_threshold(int i_low_threshold)
{
  if (is_low_threshold_legal(i_low_threshold))
  {
    low_threshold = i_low_threshold;
  }
  else
  {
    Serial.println("Illegal moisture low threshold");
  }
}

void Plant::update_current_moisture_value()
{
  current_moisture_value = moisture_sensor.get_moisture_value();
}

void Plant::water_now()
{
  if (!being_watered_now)
  {
    water_pump.start_pumping();
    being_watered_now = true;
  }

  delay(3000);
}

void Plant::stop_water()
{
  Serial.print("being water_now:"); Serial.println(being_watered_now);
  water_pump.stop_pumping();
  being_watered_now = false;
}

void Plant::stop_watering()
{
  update_current_moisture_value();
  Serial.print("moisture val:"); Serial.println(current_moisture_value);
  stop_water();
}
