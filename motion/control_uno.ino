#include "Servo.h"
#include "string.h"

int vs = 9;
Servo motor[3];
int speed = 60; // speed=90停

void (*resetFunc)(void) = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(vs, OUTPUT);
  digitalWrite(vs, LOW);
  motor[0].attach(8);
  motor[1].attach(10);
  motor[2].attach(11);
}
char ch, buf;
int id, para;
String para_str;
void loop()
{
  if (Serial.available())
  {
    ch = Serial.read();
    id = int(ch - 48);
    buf = Serial.read();
    para_str = Serial.readStringUntil('\n');
    // if (Serial.available())
    Serial.read();
    // Serial.print(ch);
    // Serial.print(buf);
    // Serial.println(para_str);
    para = para_str.toInt();
    if (id == 5)
    {
      motor[id].writeMicroseconds(para);
      // Serial.print("motor[0] already changed to ");
      // Serial.println(para);
    }
    else if (id == 1 || id == 2)
    {
      if (para > 0)
      {
        motor[id].write(speed);
      }
      else
      {
        motor[id].write(180 - speed);
        para = -para;
      }
      delay(para);
      motor[id].write(90);
      // Serial.print("motor[");
      // Serial.print(id);
      // Serial.print("] already runned for ");
      // Serial.println(para);
    }
    else if (id == 3)
    {
      // 继电器
      if (para == 0)
      {
        digitalWrite(vs, LOW);
        // Serial.println("vs off");
      }
      else
      {
        digitalWrite(vs, HIGH);
        // Serial.println("vs on");
      }
    }
    else if (id == 4)
    {
      resetFunc();
    }
    delay(10);
  }
  // motor[0].write(0);
  // delay(2000);
  // motor[0].write(45);
  // delay(1000);
  // motor[0].write(90);
  // delay(1000);
  // motor[0].write(135);
  // delay(1000);
  // motor[0].write(180);
  // delay(1000);
}