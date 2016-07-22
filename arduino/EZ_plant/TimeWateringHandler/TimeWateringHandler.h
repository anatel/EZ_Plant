#ifndef TimeWateringHandler_h
#define TimeWateringHandler_h

#include "Arduino.h"
#include <SPI.h>
#include "../WateringHandler/WateringHandler.h"

class TimeWateringHandler : public WateringHandler
{
  private:
    int repeats;
    int repeat_every;

  public:
    TimeWateringHandler(int i_repeats, int i_repeat_every);
    virtual bool is_it_time_to_water();
};

#endif
