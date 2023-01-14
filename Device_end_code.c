static const int GPS_RXPin = 3, GPS_TXPin = 2;
static const uint32_t GPSBaud = 9600;

static const int Radio_TXPin = 10;
static const int Radio_RXPin = 11;
static const int Radio_SetPin = 12;

// Desine serial connection to radio device
SoftwareSerial HC12(Radio_TXPin, Radio_RXPin);

// The TinyGPSPlus object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(GPS_RXPin, GPS_TXPin);

int last_resp_time;
int interval;
int packet_count;

const int message_interval = 3000;

void setup() {
  pinMode(Radio_SetPin, OUTPUT);

  // Begin Computer Serial
  Serial.begin(9600);
  Serial.println("Hello");
  delay(200);
  // Begin HC-12 Serial
  Serial.println("Beginning HC-12 Serial");
  delay(200);
  
  HC12.begin(1200);               // Serial port to HC12
  delay(200);
  
  // Begin GPS Serial
  Serial.println("Beginning GPS Serial");
  delay(200);
  
  ss.begin(GPSBaud);
  delay(200);
  
  // Begin MPU
  Serial.println("Beginning MPU Serial");
  delay(200);
  
  mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G);
  delay(200);

  // Set transmission mode
  Serial.println("Adjutsing Radio Settings");
  delay(200);
  
  digitalWrite(Radio_SetPin, LOW); //Set AT Command Mode
  delay(200);
  HC12.print("AT+FU4");               // Send AT Command to HC-12
  delay(200);
  HC12.print("AT+P8");               // Send AT Command to HC-12
  delay(200);
  digitalWrite(Radio_SetPin, HIGH);          // Exit AT Command mode

  last_resp_time = millis();
  packet_count = 0;

  Serial.println("Startup Complete");
}

void loop() {
  interval = millis() - last_resp_time;
  if (interval >= message_interval) {

    sendMessage();

    //Reset last response time
    last_resp_time = millis();
  }

  while (interval < message_interval) {
    if (ss.available() > 0) {
      gps.encode(ss.read());
    }
    interval = millis() - last_resp_time;
  }

}

void sendMessage() {
  // Char array object to store temp information
  char temp_char[60];

  String temp_message = getLocation();
  temp_message += ",";
  temp_message += getSatCount();
  temp_message += ",";
  temp_message += getHdop();
  temp_message += ",";
  temp_message += getMDY();
  temp_message += ",";
  temp_message += getHMSC();
  temp_message += ",";
  temp_message += getTemp();
  temp_message += ",";
  temp_message += String(packet_count);

  temp_message.toCharArray(temp_char, 60);
  HC12.write(temp_char);

  Serial.print("Sent Message");
  Serial.write(temp_char);

  // Increment Packet Count
  packet_count += 1;
}

String getLocation() {
  if (gps.location.isValid()) {
    return String(gps.location.lat(), 6) + "," + String(gps.location.lng(), 6);
  } else {
    return "NA,NA";
  }
}

String getSatCount() {
  if (gps.location.isValid()) {
    return String(gps.satellites.value());
  } else {
    return "NA";
  }
}

String getMDY() {
  if (gps.date.isValid()) {
    return String(gps.date.month()) + "/" + String(gps.date.day()) + "/" + String(gps.date.year());
  } else {
    return "NA/NA/NA";
  }
}

String getHMSC() {
  if (gps.time.isValid()) {
    return String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second()) + ":" + String(gps.time.centisecond());
  } else {
    return "NA:NA:NA:NA";
  }
}

String getHdop() {
  if (gps.location.isValid()) {
    return String(gps.hdop.value());
  } else {
    return "NA";
  }
}

String getTemp() {
  return String(mpu.readTemperature());
}
