#ifndef Plant_h
#define Plant_h

#include <SPI.h>
#include "Arduino.h"
#include "../WateringHandler/WateringHandler.h"
#include "../WaterPump/WaterPump.h"
#include "../MoistureSensor/MoistureSensor.h"

class Plant
{
  private:
    const char * plant_id;
    static const int max_moisture = 1000;
    MoistureSensor moisture_sensor;
    WaterPump water_pump;
    bool being_watered_now;
    int current_moisture_value;
    int low_threshold;

  public:
    Plant();
    Plant(const char * plant_id, const char * sensor_pin_num, int water_pump_pin_num);
    bool is_it_time_to_water();
    void update_current_moisture_value();
    int get_current_moisture_value();
    void start_watering_if_needed();
    void stop_watering_if_needed();
    void set_low_threshold(int i_low_threshold);
    void water_now();
    void stop_water();
    bool is_low_threshold_legal(int threshold);
};

#endif
