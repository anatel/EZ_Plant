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

  // return root["plants"][plant_id]["water_data"]["water_mode"];
  return root["plants"][plant_id]["water_mode"];
}

long JsonParser::get_low_moisture_value(char * json, int plant_id)
{
  JsonObject& root = jsonBuffer.parseObject(json);

  // return root["plants"][plant_id]["water_data"]["low_threshold"];
  return root["plants"][plant_id]["low_threshold"];
}
