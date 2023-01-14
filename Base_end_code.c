#include <SoftwareSerial.h>

static const int Radio_TXPin = 10;
static const int Radio_RXPin = 11;
static const int Radio_SetPin = 12;

SoftwareSerial HC12(Radio_TXPin, Radio_RXPin); // HC-12 TX Pin, HC-12 RX Pin

void setup() {
  Serial.begin(9600);             // Serial port to computer
  HC12.begin(1200);               // Serial port to HC12

  pinMode(Radio_SetPin, OUTPUT);

  // Set transmission mode
  digitalWrite(Radio_SetPin, LOW); //Set AT Command Mode
  delay(200);
  HC12.print("AT+FU4");               // Send AT Command to HC-12
  delay(200);
  HC12.print("AT+P8");               // Send AT Command to HC-12
  delay(200);
  digitalWrite(Radio_SetPin, HIGH);          // Exit AT Command mode
  

  Serial.println("Started Listening");
}

void loop() {
  while (HC12.available()) {        // If HC-12 has data
    Serial.write(HC12.read());      // Send the data to Serial monitor
  }
}
