#ifndef MoistureWateringHandler_h
#define MoistureWateringHandler_h

#include "Arduino.h"
#include <SPI.h>
#include "../WateringHandler/WateringHandler.h"

class MoistureWateringHandler : public WateringHandler
{
  private:
    int low_threshold;

  public:
    MoistureWateringHandler(int i_low_threshold);
    virtual bool is_it_time_to_water();
};

#endif
