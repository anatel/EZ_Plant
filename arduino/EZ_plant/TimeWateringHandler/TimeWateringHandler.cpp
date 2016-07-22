#include "TimeWateringHandler.h"

TimeWateringHandler::TimeWateringHandler(int i_repeats, int i_repeat_every)
{
  repeats = i_repeats;
  repeat_every = i_repeat_every;
}

bool TimeWateringHandler::is_it_time_to_water()
{
  return false;
}
