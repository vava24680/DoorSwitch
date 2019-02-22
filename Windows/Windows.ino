#include <Bridge.h>

int press_delay = 350;

char pin13[2];
char valueStr[2];
int valueInt;

int Switch_state=0;

void setup() {
    pinMode(13,OUTPUT);
    pinMode(3,OUTPUT);
    pinMode(12,OUTPUT);

    Bridge.begin();   // Pins 0 and 1 should be avoided as they are used by the Bridge library.
}
 
void loop() {
    Bridge.get("Reg_done",  pin13, 2);
    digitalWrite(13, atoi(pin13));    

    Bridge.get("Switch",  valueStr, 2);
    if (strcmp(valueStr,"") != 0){
        valueStr[1]='\0';
        valueInt = atoi(valueStr);
        if (valueInt >= 1 && Switch_state <= 0){
            digitalWrite(3, HIGH);        
            delay(press_delay);
            digitalWrite(3, LOW);        
            Switch_state = 1;
        }
        else if ((valueInt == 0 && Switch_state >= 1)){
            digitalWrite(12, HIGH);
            delay(press_delay);
            digitalWrite(12, LOW);
            Switch_state = 0;
        }
        Bridge.put("Switch", "");
    }
}
