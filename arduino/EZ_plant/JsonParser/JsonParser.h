#ifndef JsonParser_h
#define JsonParser_h

#include "Arduino.h"
#include <ArduinoJson.h>

class JsonParser
{
  public:
    JsonParser();
    JsonObject& create_json_to_post(const char * username, const char * plant_id, int moisture);
    const char * get_watering_mode(char * json, int plant_index);
    long get_low_moisture_value(char * json, int plant_index);
    long get_plant_count(char * json);
    long get_water_pump_port(char * json, int plant_index);
    const char * get_moisture_sensor_port(char * json, int plant_index);
    bool get_water_now(char * json, int plant_index);
    const char * get_plant_id(char * json, int plant_index);
};

#endif
