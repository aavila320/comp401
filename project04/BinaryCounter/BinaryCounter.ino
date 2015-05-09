// Binary Counter for Arduino
// Project04 - Comp 401

int button = 2;                            // button connects at pin 2
int presses = 0;                           // counts the number of presses
long time = 0;			
long debounce = 100;	                   // how many ms to "debounce"
const byte numPins = 8;                    // number of LEDs used
int state;                                 // state of pins - high and low
byte pins[] = {5, 6, 7, 8, 9, 10, 11, 12}; // pins to connect leds on Arduino
 
void setup()
{
	for(int i = 0; i < numPins; i++) {
		pinMode(pins[i], OUTPUT);
	}
	pinMode(button, INPUT);
	attachInterrupt(0, count, LOW);
}
// convert button presses to binary and store in string 
void loop()
{
	String binNumber = String(presses, BIN);
	int binLength = binNumber.length();	// determine length of string
	if(presses <= 255) {
		for(int i = 0, x = 1; i < binLength; i++, x+=2) { 
			if(binNumber[i] == '0') state = LOW;
			if(binNumber[i] == '1') state = HIGH;
			digitalWrite(pins[i] + binLength - x, state);
		}	
	} 
        else {}
}
 
// counts button presses
void count() { 
	// increase presses and "debounce" button
	if(millis() - time > debounce)	presses++;
	time = millis();
}
