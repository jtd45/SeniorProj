//Sketch to control pan/tilt servo motor for camcorder
//must be able to read information from a serial
//and adjust the position of the serial motors 

/***
 * The read will occur in this manner..
 * one byte will be read. the first four MSB bits will control
 * the pan servo. The four LSB will control the tilt servo.
 * 00010001 = add 1 position to both servos
 * 10101100 = subtract 2 from pan, subtract 4 from tilt.
 */
#include <Servo.h>

//10011001 = 0x99 minus 1 each
//00010001 = 0x11 plus 1 each

Servo panservo;
Servo tiltservo;

String pos;
int readByte = 0;
int panadjust = 0;
int tiltadjust = 0;
int pan = 90;
int tilt = 90;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  panservo.attach(9);
  tiltservo.attach(10);
}

void loop() {
  // put your main code here, to run repeatedly:
  if( Serial.available() > 0){
        readByte = Serial.read();

        Serial.println((char)readByte);
        switch(readByte){
          case '8':
            tilt=tilt+3;
            break;
          case '2':
            tilt=tilt-3;
            break;
          case '6':
            pan=pan+3;
            break;
          case '4':
            pan=pan-3;
            break;
          case '+':
            pan = pan +3;
            tilt = tilt +3;
            break;
          case '-':
            pan = pan -3;
            tilt = tilt -3;
            break;
          default:
            panadjust = (readByte & 0xF0) >> 4;
            tiltadjust = (readByte & 0x0F);
            Serial.println(readByte, HEX);
            Serial.println(panadjust, HEX);
            Serial.println(tiltadjust, HEX);
            //adjust pan
            if( (panadjust & 0x08) > 0 ){
              //subtract
              pan = pan - (panadjust & 0x07);
              if(pan<5) pan =5;
            }
            else {
              pan = pan + panadjust;
              if(pan>175) pan = 175;
            }
    
            //adjust tilt
            if((tiltadjust & 0x08) > 0){
              //subtract
              tilt = tilt - (tiltadjust &0x07);
            }
            else {
              tilt = tilt + tiltadjust;
            }
            if(readByte == '0'){
              //reset
              pan = 90;
              tilt = 90;
            }
            break;
        }
        if(tilt>110) tilt = 110;
        if(tilt<45) tilt = 45;
        pos = "pan: "+(String)pan+", tilt: "+(String)tilt;
        Serial.println(pos);
  }
  panservo.write(pan);
  delay(5);
  tiltservo.write(tilt);
  
  delay(13);

}
