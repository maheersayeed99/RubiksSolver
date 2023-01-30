#include <Stepper.h>                  // Stepper Motor

const int stepsPerRevolution = 200;   // Stepper

#define IN1 5                         // Stepper Pins
#define IN2 4
#define IN3 13
#define IN4 15

#define DC1 0                         // DC Motor Pins
#define DC2 2

#define ENC1 14                       // Encoder Pins
#define ENC2 12


// VARIABLES
int pos = 0;            // Encoder Position
int ceiling = 254;
int deadband = 45;
int setPoint = 0;
int activatePoint = 0;
int disabledPoint = 1176/2;
/*
float kp = .5;
float kd = .1;
float ki = .01;
*/
int count = 0;


float kp = 2;
float kd = .4;
float ki = .01;




float u = 0;

int prevError = 0;

float error = 0;
float derror = 0;
float ierror = 0;


long currTime;
long prevTime;
float timePassed;

int testVal = 130;


// HELPER FUNCTIONS

void ICACHE_RAM_ATTR updateEncoder(); 
void powerMotor(int pwmVal, bool power = true);


Stepper myStepper(stepsPerRevolution, IN1, IN2, IN3, IN4);    // Initialize Stepper Motor


void setup() {
  

  Serial.begin(115200);       // Serial port open
  
  myStepper.setSpeed(60);     // Initialize Stepper Speed

  pinMode(ENC1, INPUT);       // Encoder pins are inputs
  pinMode(ENC2, INPUT);  
  
  pinMode(DC1, OUTPUT);       // DC Motor pins are outputs
  pinMode(DC2, OUTPUT);
  
  attachInterrupt(digitalPinToInterrupt(ENC1), updateEncoder, RISING);  // Encoder pin used as interrupt calls updateEncoder function 

  
  trayActivateCW();
  delay(250);
  trayActivateCCW();
  
  pos = 0; // Initialize encoder position
  prevTime = 0;
  prevError = 0;
  setPoint = -1176/2;
  u = 0;
  

}

void loop() {
  
  waitForInput();
  Serial.print(pos);
  Serial.print("   ");
  Serial.print(activatePoint);
  Serial.print("  ");
  Serial.print(disabledPoint);
  Serial.print("  ");
  Serial.print(setPoint);
  Serial.println("  ");
  
  delay(200);
    
}





// FUNCTION TO TRACK ENCODER POSITION
void updateEncoder(){
  int b = digitalRead(ENC2);
  if (b>0){
    pos ++;
  }
  else{
    pos --;
  }
}

// FUNCTION TO INPUT DC MOTOR POWER
void powerMotor(int pwmVal, bool power){

  if (power == false){
    digitalWrite(DC1, LOW);
    digitalWrite(DC2, LOW);
    return;
  }

  if (pwmVal < 0){
    analogWrite(DC1, -pwmVal);
    digitalWrite(DC2,LOW);
  }

  else if (pwmVal > 0){
    analogWrite(DC2, pwmVal);
    digitalWrite(DC1,LOW);    
  }

  else{
    digitalWrite(DC1, LOW);
    digitalWrite(DC2, LOW);
  }
}




// FUNCTION THAT TAKES SERIAL INPUT TO MAKE A MOVE

void waitForInput(){
  
  if (Serial.available() > 0) {
    // Read the data from the serial buffer
    char input = Serial.read();

    switch (input) {
      case 'R':
        right(-1);
        break;

      case 'r':
        right(1);
        break;

      case '3':
        right(0);
        break;


      case 'L':
        left(-1);
        break;

      case 'l':
        left(1);
        break;

      case '1':
        left(0);
        break;


      case 'T':
        top(-1);
        break;

      case 't':
        top(1);
        break;

      case '0':
        top(0);
        break;


      case 'D':
        bottom(-1);
        break;

      case 'd':
        bottom(1);
        break;

      case '5':
        bottom(0);
        break;


      case 'F':
        front(-1);
        break;

      case 'f':
        front(1);
        break;

      case '2':
        front(0);
        break;


      case 'B':
        back(-1);
        break;

      case 'b':
        back(1);
        break;

      case '4':
        back(0);
        break;


      case 'i':
        trayActivateCW();
        break;

      case 'o':
        trayActivateCCW();
        break;

      case 'p':
        trayActivate180();
        break;


      case 'I':
        trayDisabledCW();
        break;

      case 'O':
        trayDisabledCCW();
        break;

      case 'P':
        trayDisabled180();
        break;


      case ';':
        Serial.println("Working Input");
        break;

      case '<':
        Serial.println("Right");
        testVal -= 1;
        break;

      case '-':
        Serial.println("Stop");
        powerMotor(0,20);
        break;

      case '>':
        Serial.println("Right");
        testVal += 1;
        break;

      case ',':
        Serial.println("activate");
        activateShroud();
        break;

      case '.':
        Serial.println("disable");
        disableShroud();
        break;

      case '/':
        Serial.println("flip");
        flipShroud();
        break;
      
      default:
        // Code to execute if input is not 1, 2, or 3
        break;
    }
  }
  
}


// ACTIVATED SHROUD MOVE FUNCTIONS

void trayActivateCW(){
  myStepper.step(53);
  delay(50);
  myStepper.step(-3);
  delay(250);
  return;
}

void trayActivateCCW(){
  myStepper.step(-51);
  delay(50);
  myStepper.step(1);
  delay(250);
  return;
}

void trayActivate180(){
  myStepper.step(102);
  delay(50);
  myStepper.step(-2);
  delay(250);
  return;
}



// DISABLED SHROUD MOVE FUNCTIONS


void trayDisabledCW(){
  myStepper.step(50);
  delay(250);
  return;
}

void trayDisabledCCW(){
  myStepper.step(-50);
  delay(250);
  return;
}

void trayDisabled180(){
  myStepper.step(100);
  delay(250);
  return;
}





// FUNCTION TO RUN PID

void pidLoop(){
  
  currTime = micros();
  timePassed = ((float)currTime-prevTime)/1.0e6;
  prevTime = currTime;
  
  
  error = pos - setPoint;
  derror = (error-prevError)/timePassed;
  ierror = ierror + error*timePassed;

  prevError = error;
  
  /*
  if (fabs(error)<5){
    u = 0;
    return;
  }
  */

  u = kp*error + kd*derror + ki*ierror;
  
  if (u > 0)
  {
    u += deadband;
  }
  else if (u<=0)
  {
    u -= deadband;
  }

  if (u>ceiling)
  {
    u = ceiling;
  }
  else if (u<-ceiling)
  {
    u = -ceiling;
  }
}


void moveShroud(int newSet){
  setPoint = newSet;
  error = pos - setPoint;
  derror = 0;
  ierror = 0;
  while(fabs(error) > 10)
  {
    pidLoop();

    Serial.print(activatePoint);
    Serial.print("  ");
    Serial.print(disabledPoint);
    Serial.print("  ");
    Serial.print(setPoint);
    Serial.print("  ");

    Serial.print(pos);
    Serial.print("  ");
    Serial.print(error);
    Serial.print("  ");
    Serial.print(derror);
    Serial.print("  ");
    Serial.print(ierror);
    Serial.print("  ");
    Serial.print(u);
    Serial.println("  ");
    
    powerMotor(u);
    delay(20);
  }
  powerMotor(0, false);
}


void flipShroud(){
  
  moveShroud(activatePoint);
  delay(10);
  pos += 1190;
  count ++;
  if (count % 8 == 0){
    pos -= 31;
  }
  
  if (count % 40 == 0){
    pos -= 20;
  }
  
  delay(10);
  //activatePoint -= 1176;
  //disabledPoint -= 1176;
  moveShroud(disabledPoint);

  delay(250);
  return;
}

void activateShroud(){
  moveShroud(activatePoint-0);
  delay(250);
  return;
}

void disableShroud(){
  moveShroud(disabledPoint+0);
  delay(250);
  return;
}





// MOVES

void left(int dir){
  disableShroud();
  trayDisabledCW();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayActivateCCW();
  }
  else if (dir == -1){
    trayActivateCW();
  }
  else{
    trayActivate180();
  }

}



void right(int dir){
  disableShroud();
  trayDisabledCCW();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayActivateCCW();
  }
  else if (dir == -1){
    trayActivateCW();
  }
  else{
    trayActivate180();
  }

}


void top(int dir){
  flipShroud();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayActivateCCW();
  }
  else if (dir == -1){
    trayActivateCW();
  }
  else{
    trayActivate180();
  }
}


void bottom(int dir){

  activateShroud();
  
  if (dir == 1){
    trayActivateCCW();
  }
  else if (dir == -1){
    trayActivateCW();
  }
  else{
    trayActivate180();
  }

}


void front(int dir){

  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayActivateCCW();
  }
  else if (dir == -1){
    trayActivateCW();
  }
  else{
    trayActivate180();
  }
}


void back(int dir){

  disableShroud();
  trayDisabled180();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayActivateCCW();
  }
  else if (dir == -1){
    trayActivateCW();
  }
  else{
    trayActivate180();
  }
}
