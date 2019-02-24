#include <Bridge.h>

int press_delay = 350;

char pin13[2];
char valueStr[2];
int valueInt;

int Switch_state = 0;

void setup() {
    pinMode(12, OUTPUT);
    pinMode(13, OUTPUT);
    Serial.begin(9600);
    Bridge.begin();   // Pins 0 and 1 should be avoided as they are used by the Bridge library.
}

void loop() {
    Bridge.get("Reg_done",  pin13, 2);
    digitalWrite(13, atoi(pin13));

    Bridge.get("Open",  valueStr, 2);
    if (strcmp(valueStr,"") != 0){
        valueStr[1]='\0';
        valueInt = atoi(valueStr);
        Serial.print("received value: ");
        Serial.println(valueInt);
        if (valueInt >= 1 && Switch_state <= 0){
            digitalWrite(12, HIGH);
            delay(press_delay);
            digitalWrite(12, LOW);
        }
        Bridge.put("Open", "");
    }
}
