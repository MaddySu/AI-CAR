//Intractive bom        // Led in NodeMCU at pin GPIO16 (D0).
void setup() {
pinMode(2, OUTPUT);    // LED pin as output.
}
void loop() {
digitalWrite(2, HIGH);// turn the LED off.(Note that LOW is the voltage level but actually 
                        //the LED is on; this is because it is acive low on the ESP8266.
delay(1000);            // wait for 1 second.
digitalWrite(2, LOW); // turn the LED on.
delay(1000); // wait for 1 second.
}