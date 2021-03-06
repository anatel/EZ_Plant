#ifndef WebClient_h
#define WebClient_h

#include "Arduino.h"
#include <WiFi.h>
#include <SPI.h>
#include "../JsonParser/JsonParser.h"

class WebClient
{
  private:
    IPAddress server;
    int port;
    WiFiClient client;

    IPAddress get_ip_address_from_string(char * ip_address);
    void init_wifi(char * ssid, char * pass);
    void print_wifi_status();

  public:
    WebClient();
    WebClient(char * address, int i_port, char * ssid, char * pass);
    void post_data_to_server(String route);
    char * get_json_from_server(String route);
    void post_json_to_server(JsonObject& json, String route);
    void close_server_connection();
};

#endif
