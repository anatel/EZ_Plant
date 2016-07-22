#ifndef WateringHandler_h
#define WateringHandler_h

#include "Arduino.h"
#include <SPI.h>

class WateringHandler
{
  protected:
    int current_moisture_value;

  public:
    WateringHandler();
    int get_current_moisture_value();
    void update_current_moisture_value(int new_moisture_value);
    virtual bool is_it_time_to_water() = 0;
};

#endif
