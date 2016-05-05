#include "Arduino.h"
#include "JsonParser.h"

JsonParser::JsonParser() {}

JsonObject& JsonParser::create_json_from_moisture_values(int plant_id, int moisture_value)
{
  JsonObject& root = jsonBuffer.createObject();
  root["plant_id"] = plant_id;
  root["moisture_value"] = moisture_value;

  return root;
}
