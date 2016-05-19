#include <MoistureSensor.h>
#include <JsonParser.h>
#include <WebClient.h>

//char ssid[] = "Living The Dream_2.4";
//char pass[] = "0546757191";
char ssid[] = "xxxx";
char pass[] = "xxxx";
char address[] = "192.168.1.4";
int port = 5000;
int moisture_analog_pin_num = A0;

WebClient web_client;
MoistureSensor moisture_sensor;

void setup() 
{
  Serial.begin(9600); 
  while (!Serial) {}
  web_client = WebClient(address, port, ssid, pass);
  moisture_sensor = MoistureSensor(moisture_analog_pin_num);
}

void loop()
{
  int moisture_value;
  JsonParser json_parser;
  
  moisture_value = moisture_sensor.get_moisture_value();
  JsonObject& json_to_send = json_parser.create_json_from_moisture_values(0, moisture_value);
  web_client.post_json_to_server(json_to_send, "/push_moisture_data");
  web_client.close_server_connection();
}
