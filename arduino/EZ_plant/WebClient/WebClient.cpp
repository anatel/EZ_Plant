#include "Arduino.h"
#include "WebClient.h"

WebClient::WebClient() {}

WebClient::WebClient(char * address, int i_port, char * ssid, char * pass)
{
  server = get_ip_address_from_string(address);
  init_wifi(ssid, pass);
  port = i_port;
}

IPAddress WebClient::get_ip_address_from_string(char * ip_address)
{
  uint8_t first_octet;
  uint8_t second_octet;
  uint8_t third_octet;
  uint8_t fourth_octet;
  char * curr_octet;

  curr_octet = strtok(ip_address, ".");
  first_octet = atoi(curr_octet);
  curr_octet = strtok(NULL, ".");
  second_octet = atoi(curr_octet);
  curr_octet = strtok(NULL, ".");
  third_octet = atoi(curr_octet);
  curr_octet = strtok(NULL, ".");
  fourth_octet = atoi(curr_octet);

  return IPAddress(first_octet, second_octet, third_octet, fourth_octet);
}

void WebClient::init_wifi(char * ssid, char * pass)
{
  int status = WL_IDLE_STATUS;

  if (WiFi.status() == WL_NO_SHIELD)
  {
    Serial.println("WiFi shield not present");
    while(true);
  }

  while (status != WL_CONNECTED)
  {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }

  Serial.println("Connected to wifi");
  print_wifi_status();
}

void WebClient::print_wifi_status()
{
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

void WebClient::post_json_to_server(JsonObject& json, String route)
{
  // Serial.println("\nStarting connection to server...");
  if (client.connect(server, port))
  {
    // Serial.println("connected to server");
    client.println("POST " + route + " HTTP/1.1");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(json.measureLength());
    client.println();
    // json.printTo(Serial);
    // Serial.println(json.measureLength());
    json.printTo(client);
    client.println();
  }
}

char * WebClient::get_json_from_server(String route)
{
  char c;
  char json[400] = "";
  int i = 0;
  bool json_started = false;

  Serial.println("\nStarting connection to server...");
  if (client.connect(server, port))
  {
    Serial.println("connected to server");
    client.println("GET " + route + " HTTP/1.1");
    client.println("User-Agent: ArduinoWiFi/1.1");
    client.println("Connection: close");
    client.println();
  }

  delay(10000);

  while(client.available())
  {
    c = client.read();
    if (json_started)
    {
      json[i] = c;
      i++;
    }
    else
    {
      if (c == '{')
      {
        json[i] = c;
        i++;
        json_started = true;
      }
    }
  }

  json[i] = '\0';
  return json;
}

void WebClient::close_server_connection()
{
  delay(5000);
  client.flush();
  client.stop();
}
