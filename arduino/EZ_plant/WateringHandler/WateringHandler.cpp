#include "WateringHandler.h"

WateringHandler::WateringHandler() {}

int WateringHandler::get_current_moisture_value()
{
  return current_moisture_value;
}

void WateringHandler::update_current_moisture_value(int new_moisture_value)
{
  current_moisture_value = new_moisture_value;
}
