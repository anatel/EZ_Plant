#include "Plant.h"

Plant::Plant() {}

Plant::Plant(int i_plant_id, int sensor_pin_num, int water_pump_pin_num)
{
  plant_id = i_plant_id;
  being_watered_now = false;
  moisture_sensor = MoistureSensor(sensor_pin_num);
  water_pump = WaterPump(water_pump_pin_num);
  watering_handler = NULL;
}

bool Plant::is_being_watered_now()
{
  return being_watered_now;
}

bool Plant::is_it_time_to_water()
{
  return watering_handler->is_it_time_to_water();
}

int Plant::get_current_moisture_value()
{
  return watering_handler->get_current_moisture_value();
}

void Plant::update_current_moisture_value()
{
  watering_handler->update_current_moisture_value(moisture_sensor.get_moisture_value());
}

void Plant::set_watering_handler(WateringHandler * new_watering_handler)
{
  watering_handler = new_watering_handler;
}

void Plant::start_watering_if_needed()
{
  if (watering_handler->is_it_time_to_water())
  {
    water_pump.start_pumping();
    being_watered_now = true;
  }
}

void Plant::stop_watering_if_needed()
{
  if (get_current_moisture_value() >= max_moisture)
  {
    water_pump.stop_pumping();
    being_watered_now = false;
  }
}
