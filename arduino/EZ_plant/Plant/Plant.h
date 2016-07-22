#ifndef Plant_h
#define Plant_h

#include "../WateringHandler/WateringHandler.h"
#include "../WaterPump/WaterPump.h"
#include "../MoistureSensor/MoistureSensor.h"

class Plant
{
  private:
    static const int max_moisture = 600;
    int plant_id;
    MoistureSensor moisture_sensor;
    WaterPump water_pump;
    WateringHandler * watering_handler;
    bool being_watered_now;

  public:
    Plant();
    Plant(int i_plant_id, int sensor_pin_num, int water_pump_pin_num);
    bool is_being_watered_now();
    bool is_it_time_to_water();
    void update_current_moisture_value();
    int get_current_moisture_value();
    void set_watering_handler(WateringHandler * new_watering_handler);
    void start_watering_if_needed();
    void stop_watering_if_needed();
};

#endif
