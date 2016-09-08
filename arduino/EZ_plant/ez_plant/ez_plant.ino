#include <MoistureSensor.h>
#include <WaterPump.h>
#include <Plant.h>
#include <JsonParser.h>
#include <WebClient.h>

char username[] = "xxxx";
char ssid[] = "xxxx";
char pass[] = "xxxx";
char address[] = "xxxx";

char push_params_prefix[] = "?u=xxxx&pid=";
char moisture_param[] = "&m=";
char plant_id_param[] = "&pid=";
String base_config_url = String("/get_config?username=");
String base_push_url = String("/p");
String base_report_url = String("/report?u=");
String push_url = base_push_url + push_params_prefix;
String config_url = base_config_url + username;
String report_url = base_report_url + username;
String moisture_water_mode = String("moisture");
int port = 5000;
const short SND_STATS_INTRVAL = 10;
const int MAX_SIZE_OF_JSON_RESPONSE = 3000;
short loop_count = 1;
WebClient web_client;

char * json_response, * json_response_copy;
JsonParser json_parser;
int water_pump_port, low_threshold;
const char * moisture_sensor_port, * water_mode, * plant_id;
bool water_now;
Plant plant;
WateringHandler * watering_handler;
long num_of_plants;
String water_mode_string;

char * copy_json_response(char * src_json_response)
{
  char json_response_copy[MAX_SIZE_OF_JSON_RESPONSE];

  strcpy(json_response_copy, src_json_response);
  return json_response_copy;
}

void setup()
{
  Serial.begin(9600);
  while (!Serial) {}

  web_client = WebClient(address, port, ssid, pass);
}

void loop()
{
  json_response = web_client.get_json_from_server(config_url);
  web_client.close_server_connection();

  json_response_copy = copy_json_response(json_response);
  num_of_plants = json_parser.get_plant_count(json_response_copy);

  for (int i = 0; i < num_of_plants; i++) {
    push_url = base_push_url + push_params_prefix;
    report_url = base_report_url + username;
    json_response_copy = copy_json_response(json_response);
    water_pump_port = json_parser.get_water_pump_port(json_response_copy, i);
    json_response_copy = copy_json_response(json_response);
    moisture_sensor_port = json_parser.get_moisture_sensor_port(json_response_copy, i);
    json_response_copy = copy_json_response(json_response);
    plant_id = json_parser.get_plant_id(json_response_copy, i);
    json_response_copy = copy_json_response(json_response);
    water_now = json_parser.get_water_now(json_response_copy, i);
    json_response_copy = copy_json_response(json_response);
    water_mode = json_parser.get_watering_mode(json_response_copy, i);

    plant = Plant(plant_id, moisture_sensor_port, water_pump_port);
    plant.update_current_moisture_value();

    push_url += plant_id;
    push_url += moisture_param;
    push_url += plant.get_current_moisture_value();

    Serial.println(loop_count);
    if (loop_count >= SND_STATS_INTRVAL) {
      loop_count = 1;
//      delay(1000);
      web_client.post_data_to_server(push_url);
      web_client.close_server_connection();
    }

    water_mode_string = String(water_mode);
    if (water_mode_string == moisture_water_mode) {
      json_response_copy = copy_json_response(json_response);
      low_threshold = json_parser.get_low_moisture_value(json_response_copy, i);
      plant.set_low_threshold(low_threshold);
    }

    if (water_now || plant.is_it_time_to_water()) {
        plant.water_now();
        report_url += plant_id_param;
        report_url += plant_id;
//        delay(1000);
        web_client.post_data_to_server(report_url);
        web_client.close_server_connection();
      }
    plant.stop_watering_if_needed();
  }
  loop_count++;
}
