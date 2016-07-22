#include <Time.h>
#include <TimeLib.h>
#include <MoistureSensor.h>
#include <WaterPump.h>
#include <WateringHandler.h>
#include <TimeWateringHandler.h>
#include <MoistureWateringHandler.h>
#include <Plant.h>
#include <JsonParser.h>
#include <WebClient.h>

char ssid[] = "xxxxx";
char pass[] = "xxxxx";
char username[] = "xxxxx";
char address[] = "xxxxx";
String base_config_url = String("/get_config?username=");
String config_url = base_config_url += username;
String moisture_data_url = "/push_moisture_data";
int port = 5000;

const int NUM_OF_PLANTS = 2;
const int MAX_SIZE_OF_JSON_RESPONSE = 300;
int moisture_analog_pin_num[NUM_OF_PLANTS];
int water_pump_pin_num[NUM_OF_PLANTS];

WebClient web_client;
Plant plants[NUM_OF_PLANTS];
WateringHandler *watering_handler[NUM_OF_PLANTS];

void setup()
{
  Serial.begin(9600);
  while (!Serial) {}

  moisture_analog_pin_num[0] = A0;
  moisture_analog_pin_num[1] = A1;
  water_pump_pin_num[0] = 3;
  web_client = WebClient(address, port, ssid, pass);

  for (int i = 0; i < NUM_OF_PLANTS; i++) {
    plants[i] = Plant(i, moisture_analog_pin_num[i], water_pump_pin_num[i]);
    watering_handler[i] = NULL;
  }
}

void loop()
{
  char * json_response;
  JsonParser json_parsers[NUM_OF_PLANTS * 3];
  const char * watering_mode[NUM_OF_PLANTS];
  char json_response_copies[NUM_OF_PLANTS * 2][MAX_SIZE_OF_JSON_RESPONSE];
  int low_threshold;

  json_response = web_client.get_json_from_server(config_url);
  web_client.close_server_connection();
  for (int i = 0; i < NUM_OF_PLANTS * 2; i++) {
    strcpy(json_response_copies[i], json_response);
  }

  for (int i = 0; i < NUM_OF_PLANTS; i++) {
    watering_mode[i] = json_parsers[i*2].get_watering_mode(json_response_copies[i*2], i);
//    Serial.print("Watering mode: "); Serial.println(watering_mode[i]);
    String watering_mode_string = String(watering_mode[i]);
    if (watering_mode_string == "moisture") {
      low_threshold = json_parsers[i*2+1].get_low_moisture_value(json_response_copies[i*2+1], i);
//      Serial.print("Low: "); Serial.println(low_threshold);
      watering_handler[i] = new MoistureWateringHandler(low_threshold);
      plants[i].set_watering_handler(watering_handler[i]);
      plants[i].update_current_moisture_value();
//      Serial.println(plants[i].get_current_moisture_value());
      if (plants[i].is_it_time_to_water()) {
        Serial.print("Plant"); Serial.print(i); Serial.println(": It's time to water!");
      } else {
        Serial.print("Plant"); Serial.print(i); Serial.println(": Not yet...");
      }
    } else {

    }

    JsonObject& json_to_send = json_parsers[i*2+2].create_json_from_moisture_values(i, plants[i].get_current_moisture_value());
    web_client.post_json_to_server(json_to_send, moisture_data_url);
    web_client.close_server_connection();

    delete(watering_handler[i]);
  }
}
