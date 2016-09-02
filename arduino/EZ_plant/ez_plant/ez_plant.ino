#include <MoistureSensor.h>
#include <WaterPump.h>
#include <WateringHandler.h>
#include <TimeWateringHandler.h>
#include <MoistureWateringHandler.h>
#include <Plant.h>
#include <JsonParser.h>
#include <WebClient.h>

//char ssid[] = "oneplus";
//char pass[] = "rugh_tcrvo33";
//char ssid[] = "Living The Dream_2.4";
//char pass[] = "0546757191";
//char ssid[] = "Kakopark";
//char pass[] = "5555555555";
char username[] = "anat.eliahu@gmail.com";
char ssid[] = "SmartBox-1a30";
char pass[] = "rugh_tcrvo33";
char address[] = "192.168.1.2";
char push_params_prefix[] = "?u=anat.eliahu@gmail.com&pid=";
char moisture_param[] = "&m=";
char plant_id_param[] = "&pid=";
String base_config_url = String("/get_config?username=");
String base_push_url = String("/p");
String base_report_url = String("/report?u=");
String push_url = base_push_url + push_params_prefix;
String config_url = base_config_url + username;
String report_url = base_report_url + username;
int port = 5000;
const int MAX_SIZE_OF_JSON_RESPONSE = 3000;
WebClient web_client;

char * json_response, * json_response_copy;
JsonParser json_parser;
int water_pump_port, low_threshold;
const char * moisture_sensor_port, * water_mode, * plant_id;
bool water_now;
Plant plant;
WateringHandler * watering_handler;
long num_of_plants;

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
  push_url = base_push_url + push_params_prefix;
  report_url = base_report_url + username;

  json_response = web_client.get_json_from_server(config_url);
  web_client.close_server_connection();

  json_response_copy = copy_json_response(json_response);
  num_of_plants = json_parser.get_plant_count(json_response_copy);

  for (int i = 0; i < num_of_plants; i++) {
    json_response_copy = copy_json_response(json_response);
    water_pump_port = json_parser.get_water_pump_port(json_response_copy, i);
    json_response_copy = copy_json_response(json_response);
    moisture_sensor_port = json_parser.get_moisture_sensor_port(json_response_copy, i);
    json_response_copy = copy_json_response(json_response);
    plant_id = json_parser.get_plant_id(json_response_copy, i);
    json_response_copy = copy_json_response(json_response);
    water_now = json_parser.get_water_now(json_response_copy, i);
//    json_response_copy = copy_json_response(json_response);
//    water_mode = json_parser.get_watering_mode(json_response_copy, i);

    plant = Plant(plant_id, moisture_sensor_port, water_pump_port);
    plant.update_current_moisture_value();

    push_url += plant_id;
    push_url += moisture_param;
    push_url += plant.get_current_moisture_value();

    delay(1000);
    web_client.post_data_to_server(push_url);
    web_client.close_server_connection();

    Serial.println(water_now);
    if (water_now) {
//        plant.water_now();
        report_url += plant_id_param;
        report_url += plant_id;
//        delay(1000);
        web_client.post_data_to_server(report_url);
        web_client.close_server_connection();
    } else {
//    plant.start_watering_if_needed();
    }

    plant.stop_watering_if_needed();
  }

//    String water_mode_string = String(water_mode);
//    if (water_mode_string == "moisture") {
//      json_response_copy = copy_json_response(json_response);
//      low_threshold = json_parser.get_low_moisture_value(json_response_copy, i);
//      watering_handler = new MoistureWateringHandler(low_threshold);
//      plant.set_watering_handler(watering_handler);
//    }
//
//    plant.update_current_moisture_value();
//    if (water_now) {
////      plant.water_now();
//    } else {
////      plant.start_watering_if_needed();
//    }
//
//    plant.stop_watering_if_needed();
//
////    Serial.print("pump:"); Serial.println(water_pump_port);
////    Serial.print("sensor:"); Serial.println(moisture_sensor_port);
////    Serial.print("water now:"); Serial.println(water_now);
////    Serial.print("water mode:"); Serial.println(water_mode);
////    Serial.print("id:"); Serial.println(plant_id);
////
////    strcat(url_params, "?username=");
////    strcat(url_params, username);
////    strcat(url_params, "&plant_id=");
////    strcat(url_params, plant_id);
////    strcat(url_params, "&moisture=");
////    itoa(plant.get_current_moisture_value(), current_moisture_value, 10);
////    strcat(url_params, current_moisture_value);
////
//      web_client.post_data_to_server(push_moisture_data_url, "?username=anat.eliahu@gmail.com&plant_id=VXNZTCIGMTTE&moisture=512");
//      web_client.close_server_connection();
//
//    delay(5000);
//
//    JsonObject& json_to_send = json_parser.create_json_to_post(username, plant_id, plant.get_current_moisture_value());
//    web_client.post_json_to_server(json_to_send, "/push_moisture_data");
//    web_client.close_server_connection();
//  }
//}
}
