#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// --- THÔNG TIN CẤU HÌNH ---
const char* ssid = "Bich Ngoc 2";
const char* password = "vannghivannghi";
const char* supabase_url = "https://plmqvmveaqsoxnjydcmw.supabase.co/rest/v1/sensor_data"; 
const char* supabase_key = "sb_publishable_cKeaOmTblGHGYLsmikzTnw_0JPn6Ssg";

// --- CẤU HÌNH CHÂN CẮM ---
#define SOIL_PIN 34    // Chân Aout cảm biến đất nối D34
#define DHTPIN 5       // Chân Out DHT11 nối D5
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(1000); 
  dht.begin();
  
  Serial.println("\n--- HE THONG BAT DAU HOAT DONG ---");

  // 1. Kết nối WiFi
  WiFi.begin(ssid, password);
  Serial.print("Dang ket noi WiFi");
  int wifi_retry = 0;
  while (WiFi.status() != WL_CONNECTED && wifi_retry < 20) {
    delay(500); 
    Serial.print("."); 
    wifi_retry++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[OK] WiFi Connected!");

    // 2. Đọc cảm biến DHT11
    float air_temp = 0, air_hum = 0;
    int dht_retry = 0;
    while (dht_retry < 3) {
      delay(2000); 
      air_hum = dht.readHumidity(); 
      air_temp = dht.readTemperature();
      if (!isnan(air_hum) && !isnan(air_temp)) break; 
      dht_retry++;
    }
    Serial.printf(">> KK: %.1f*C | %.1f%%\n", air_temp, air_hum);

    // 3. Đọc cảm biến độ ẩm đất (Điện dung)
    long sum = 0;
    for(int i=0; i<15; i++) { 
      sum += analogRead(SOIL_PIN); 
      delay(20); 
    }
    float avgAnalog = sum / 15.0;

    // Hiệu chuẩn: 3200 (Khô) -> 1500 (Ướt). Thay đổi số này theo thực tế đo được.
    int soilPercent = map(avgAnalog, 3200, 1500, 0, 100); 
    soilPercent = constrain(soilPercent, 0, 100);
    Serial.printf(">> Dat: %d%% (Analog: %.0f)\n", soilPercent, avgAnalog);

    // 4. Gửi dữ liệu lên Supabase
    if (!isnan(air_hum) && air_hum > 0) {
      HTTPClient http;
      http.begin(supabase_url);
      http.addHeader("Content-Type", "application/json");
      http.addHeader("apikey", supabase_key);
      http.addHeader("Authorization", String("Bearer ") + supabase_key);

      StaticJsonDocument<256> doc;
      doc["soil_moisture"]   = soilPercent;
      doc["air_temperature"] = air_temp;
      doc["air_humidity"]    = air_hum;

      String jsonStr;
      serializeJson(doc, jsonStr);
      int httpResponseCode = http.POST(jsonStr);
      
      if (httpResponseCode > 0) {
        Serial.printf("[Supabase] Success! Status: %d\n", httpResponseCode);
      } else {
        Serial.printf("[Supabase] Error: %s\n", http.errorToString(httpResponseCode).c_str());
      }
      http.end();
    } else {
      Serial.println("!! Loi doc DHT11, khong gui du lieu.");
    }
  } else {
    Serial.println("\n[Error] Khong ket noi duoc WiFi.");
  }

  Serial.println("--- CHO 15 PHUT DE LAN DO TIEP THEO ---");
}

void loop() {
  // Nghỉ 15 phút (15 * 60 * 1000 ms)
  // Trong lúc này ESP32 vẫn tiêu thụ điện ~80mA, giúp sạc dự phòng không bị tắt
  delay(15 * 60 * 1000); 

  // Khởi động lại chip để chạy lại từ đầu hàm setup()
  // Việc restart giúp hệ thống chạy "sạch" hơn, tránh lỗi WiFi lâu ngày
  ESP.restart(); 
}