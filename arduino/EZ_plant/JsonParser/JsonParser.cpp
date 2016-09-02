#include "Arduino.h"
#include "JsonParser.h"

JsonParser::JsonParser() {}

JsonObject& JsonParser::create_json_to_post(const char * username, const char * plant_id, int moisture)
{
  StaticJsonBuffer<4000> jsonBuffer;

  JsonObject& root = jsonBuffer.createObject();
  root["username"] = username;
  root["plant_id"] = plant_id;
  // root["moisture"] = moisture;

  return root;
}

const char * JsonParser::get_watering_mode(char * json, int plant_index)
{
  StaticJsonBuffer<4000> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["plants"][plant_index]["water_mode"];
}

long JsonParser::get_low_moisture_value(char * json, int plant_index)
{
  StaticJsonBuffer<4000> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["plants"][plant_index]["low_threshold"];
}

long JsonParser::get_plant_count(char * json)
{
  StaticJsonBuffer<4000> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["count"];
}

long JsonParser::get_water_pump_port(char * json, int plant_index)
{
  StaticJsonBuffer<4000> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["plants"][plant_index]["water_pump_port"];
}

const char * JsonParser::get_moisture_sensor_port(char * json, int plant_index)
{
  StaticJsonBuffer<4000> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["plants"][plant_index]["moisture_sensor_port"];
}

bool JsonParser::get_water_now(char * json, int plant_index)
{
  StaticJsonBuffer<4000> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["plants"][plant_index]["water_now"];
}

const char * JsonParser::get_plant_id(char * json, int plant_index)
{
  StaticJsonBuffer<4000> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);

  return root["plants"][plant_index]["plant_id"];
}
