
#include <Arduino.h>
#include <Wire.h>
#include <BMP180MI.h>
#define I2C_ADDRESS 0x77

#include <DS3231.h>

//DS3231 - Temperature library (DS3231_test - example)
//BMP180 - Pressure library (BMP180_12C - example)

// the setup routine runs once when you press reset:


int proximityPin = 9;
int delay = 1000;
int missionTime = 0;
int timeout = 100;

//create an BMP180 object using the I2C interface
BMP180I2C bmp180(I2C_ADDRESS);

DS3231 clock;
RTCDateTime dt;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  //light sensor
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
  
  //proximity sensor
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
  pinMode(proximityPin, INPUT);

  //proximity sensor ground
  pinMode(6, OUTPUT);
  digitalWrite(6, LOW);

    //wait for serial connection to open (only necessary on some boards)
  while (!Serial);

  Wire.begin();

  //begin() initializes the interface, checks the sensor ID and reads the calibration parameters.  
  if (!bmp180.begin())
  {
    Serial.println("begin() failed. check your BMP180 Interface and I2C Address.");
    while (1);
  }

  //reset sensor to default parameters.
  bmp180.resetToDefaults();

  //enable ultra high resolution mode for pressure measurements
  bmp180.setSamplingMode(BMP180MI::MODE_UHR);
  
  clock.begin();
  clock.setDateTime(__DATE__, __TIME__);
}

// the loop routine runs over and over again forever:
void loop() {
	
	if(Serial.available()){
		int command=Serial.read();

		if(command==1){
			delay = Serial.read();
			timeout = Serial.read();
		}
		if(command==2){
			zakonczMisje();
		}
	}
	
	if(missionTime > timeout){
		zakonczMisje();
	}

  int proximityValue = digitalRead(proximityPin);
  if(proximityValue == 0 ){
      ominPrzeszkode();
    }
  
	dt = clock.getDateTime();
 
	Serial.print(clock.dateFormat("d-m-Y;H:i:s", dt));
	Serial.print(";");
  
  // read the input on analog pin 0 - light level:
  int lightValue = analogRead(A0);
  
  // print out the value you read:
  //Serial.print("light level: ");
  Serial.print(lightValue);
  Serial.print(";");

  //Serial.print("Temperature: "); 
  Serial.print(bmp180.getTemperature()); 
  //Serial.println(" degC");  
  Serial.print(";");

  //Serial.print("Pressure: "); 
  Serial.print(bmp180.getPressure());
  //Serial.println(" Pa");
  Serial.print(";");
  
  Serial.println();
  
  missionTime++;
  
  delay(delay);        // delay in between reads for stability
  
  //czas, poziom oświetlenia, temperatura, ciśnienie
  //19-12-2018;15:25:31;
}

void ominPrzeszkode() {
	Serial.println("przeszkoda");
}

void zakonczMisje() {
	Serial.println("koniec");
}