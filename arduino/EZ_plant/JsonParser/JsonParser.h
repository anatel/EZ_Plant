#ifndef JsonParser_h
#define JsonParser_h

#include "Arduino.h"
#include <ArduinoJson.h>

class JsonParser
{
  private:
    StaticJsonBuffer<200> jsonBuffer;

  public:
    JsonParser();
    JsonObject& create_json_from_moisture_values(int plant_id, int moisture_value);
};

#endif
