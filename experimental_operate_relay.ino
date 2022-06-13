/* Experiment Group - ACM0 */

int IN1 = 7;  // relay 1
int IN2 = 6;  // relay 2
int IN3 = 5;  // relay 3
int IN4 = 4;  // relay 4

int level1 = 0;
int level2 = 0;
int level3 = 0;
int level4 = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // set relay
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Turn On mortor
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  
  delay(10000); // delay 10sec
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {
    String relay_str = Serial.readStringUntil(0x0a);
    //String relay_str = Serial.readStringUntil('\n');

    int relay_array = relay_str.substring(0,4).toInt();
    int temp = 0;
    level1 = relay_array / 1000;
    temp = relay_array % 1000;
    level2 = temp / 100;
    temp = temp % 100;
    level3 = temp / 10;
    temp = temp % 10;
    level4 = temp;

    Serial.println("get: " + relay_str + ", lv1:" + level1 + ", lv2:" + level2 + ", lv3:" + level3 + ", lv4:" + level4);

    //50inch
    if(level1 == 3)  //150ml
    {
      digitalWrite(IN1, HIGH);
      delay(10870);
      digitalWrite(IN1, LOW);
    }
    else if(level1==2) //100ml
    {
      digitalWrite(IN1, HIGH);
      delay(6310);
      digitalWrite(IN1, LOW);
    }
    else if(level1==1) //50ml
    {
      digitalWrite(IN1, HIGH);
      delay(4410);
      digitalWrite(IN1, LOW);
    }
    else{
      digitalWrite(IN1, LOW);
    }
  
    //100inch 
    if(level2 == 3) //150ml
    {
      digitalWrite(IN2, HIGH);
      delay(14270);
      digitalWrite(IN2, LOW);
    }
    else if(level2 == 2) //100ml
    {
      digitalWrite(IN2, HIGH);
      delay(10340);
      digitalWrite(IN2, LOW);
    }
    else if(level2 == 1) //50ml
    {
      digitalWrite(IN2, HIGH);
      delay(5810);
      digitalWrite(IN2, LOW);
    }
    else{
      digitalWrite(IN2, LOW);
    }
  
    //200inch
    if(level3 == 3) //150ml
    {
      digitalWrite(IN3, HIGH);
      delay(16430);
      digitalWrite(IN3, LOW);
    }
    else if(level3 == 2) //100ml
    {
      digitalWrite(IN3, HIGH);
      delay(12080);
      digitalWrite(IN3, LOW);
    }
    else if(level3 == 1) //50ml
    {
      digitalWrite(IN3, HIGH);
      delay(7720);
      digitalWrite(IN3, LOW);
    }
    else{
      digitalWrite(IN3, LOW);
    }
  
    //400inch
    if(level4 == 3) //150ml
    {
      digitalWrite(IN4, HIGH);
      delay(22820);
      digitalWrite(IN4, LOW);
    }
    else if(level4 == 2) //100ml
    {
      digitalWrite(IN4, HIGH);
      delay(18290);
      digitalWrite(IN4, LOW);
    }
    else if(level4 == 1) //50ml
    {
      digitalWrite(IN4, HIGH);
      delay(16300);
      digitalWrite(IN4, LOW);
    }
    else{
      digitalWrite(IN4, LOW);
    }
    delay(60000);  // delay 10min
  }
}
