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

const char * JsonParser::get_watering_mode(char * json, int plant_id)
{
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["config"][plant_id]["watering_mode"];
}

long JsonParser::get_low_moisture_value(char * json, int plant_id)
{
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["config"][plant_id]["low"];
}
