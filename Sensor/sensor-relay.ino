#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// ========= WIFI =========
const char* ssid = "Bich Ngoc 2";
const char* password = "vannghivannghi";

// ========= SUPABASE =========
const char* sensor_url  = "https://plmqvmveaqsoxnjydcmw.supabase.co/rest/v1/sensor_data";
const char* command_url = "https://plmqvmveaqsoxnjydcmw.supabase.co/rest/v1/control_commands";
const char* supabase_key = "sb_publishable_cKeaOmTblGHGYLsmikzTnw_0JPn6Ssg";

// ========= PIN =========
#define SOIL_PIN 34
#define DHTPIN 5
#define DHTTYPE DHT11
#define RELAY_PIN 13

DHT dht(DHTPIN, DHTTYPE);

// CONFIG 
int PUMP_DURATION = 8000; 

// TIME
unsigned long lastSendTime = 0;
const unsigned long SEND_INTERVAL = 15 * 60 * 1000; // 15 phút

unsigned long lastCheckTime = 0;
const unsigned long CHECK_INTERVAL = 5000; //5 giây

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // tắt 

  dht.begin();

  Serial.println("\n--- HE THONG BAT DAU ---");

  // ===== WIFI =====
  WiFi.begin(ssid, password);
  Serial.print("Dang ket noi WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n[OK] WiFi Connected");

  sendSensorData();
}

// =========================
void loop() {

  unsigned long currentMillis = millis();

  if (currentMillis - lastSendTime >= SEND_INTERVAL) {
    lastSendTime = currentMillis;
    sendSensorData();
  }

  if (currentMillis - lastCheckTime >= CHECK_INTERVAL) {
    lastCheckTime = currentMillis;
    checkCommand();
  }
}


void sendSensorData() {

  Serial.println("\n--- DOC CAM BIEN ---");

  float air_temp = 0, air_hum = 0;

  for (int i = 0; i < 3; i++) {
    delay(2000);
    air_hum = dht.readHumidity();
    air_temp = dht.readTemperature();
    if (!isnan(air_hum) && !isnan(air_temp)) break;
  }

  long sum = 0;
  for (int i = 0; i < 15; i++) {
    sum += analogRead(SOIL_PIN);
    delay(20);
  }

  float avgAnalog = sum / 15.0;
  int soilPercent = map(avgAnalog, 3200, 1500, 0, 100);
  soilPercent = constrain(soilPercent, 0, 100);

  Serial.printf(">> KK: %.1f*C | %.1f%%\n", air_temp, air_hum);
  Serial.printf(">> Dat: %d%%\n", soilPercent);

  if (!isnan(air_hum) && air_hum > 0) {
    HTTPClient http;
    http.begin(sensor_url);

    http.addHeader("Content-Type", "application/json");
    http.addHeader("apikey", supabase_key);
    http.addHeader("Authorization", String("Bearer ") + supabase_key);

    StaticJsonDocument<256> doc;
    doc["soil_moisture"] = soilPercent;
    doc["air_temperature"] = air_temp;
    doc["air_humidity"] = air_hum;

    String jsonStr;
    serializeJson(doc, jsonStr);

    int code = http.POST(jsonStr);

    Serial.print("[Sensor] Status: ");
    Serial.println(code);

    http.end();
  }
}

void checkCommand() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi lost!");
    return;
  }

  HTTPClient http;

  String url = String(command_url) +
               "?status=eq.PENDING&order=created_at.asc&limit=1";

  http.begin(url);
  http.addHeader("apikey", supabase_key);
  http.addHeader("Authorization", String("Bearer ") + supabase_key);

  int code = http.GET();

  if (code != 200) {
    Serial.println("No command");
    http.end();
    return;
  }

  String payload = http.getString();

  if (payload.length() < 5) {
    Serial.println("Empty command");
    http.end();
    return;
  }

  Serial.println("\n Command found!");


  int idStart = payload.indexOf("id\":\"") + 5;
  int idEnd = payload.indexOf("\"", idStart);

  if (idStart < 5 || idEnd < 0) {
    Serial.println("Parse ID error");
    http.end();
    return;
  }

  String cmd_id = payload.substring(idStart, idEnd);


  if (payload.indexOf("PUMP_ON") > 0) {
    runPump();
    markExecuted(cmd_id);
  }

  http.end();
}


void runPump() {

  Serial.println("PUMP ON");

  digitalWrite(RELAY_PIN, HIGH);
  delay(PUMP_DURATION);
  digitalWrite(RELAY_PIN, LOW);

  Serial.println("PUMP OFF");
}

void markExecuted(String id) {

  HTTPClient http;

  String url = String(command_url) + "?id=eq." + id;

  http.begin(url);

  http.addHeader("Content-Type", "application/json");
  http.addHeader("apikey", supabase_key);
  http.addHeader("Authorization", String("Bearer ") + supabase_key);
  http.addHeader("Prefer", "return=minimal");

  
  String body = "{\"status\":\"EXECUTED\"}";

  int code = http.PATCH(body);

  Serial.print("Update status: ");
  Serial.println(code);

  http.end();
}