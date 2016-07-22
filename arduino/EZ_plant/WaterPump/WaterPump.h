#ifndef WaterPump_h
#define WaterPump_h

#include "Arduino.h"
#include <SPI.h>

class WaterPump
{
  private:
    int digital_pin_num;

  public:
    WaterPump();
    WaterPump(int i_digital_pin_num);
    void start_pumping();
    void stop_pumping();
};

#endif
