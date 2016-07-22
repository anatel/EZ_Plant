#include "MoistureWateringHandler.h"

MoistureWateringHandler::MoistureWateringHandler(int i_low_threshold)
{
  low_threshold = i_low_threshold;
}

bool MoistureWateringHandler::is_it_time_to_water()
{
  return current_moisture_value <= low_threshold;
}
