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
int deadband = 116;
int setPoint = 0;

float kp = 1;
float kd = 100;
float ki = 0;
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
  
  myStepper.setSpeed(75);     // Initialize Stepper Speed

  pinMode(ENC1, INPUT);       // Encoder pins are inputs
  pinMode(ENC2, INPUT);  
  
  pinMode(DC1, OUTPUT);       // DC Motor pins are outputs
  pinMode(DC2, OUTPUT);
  
  attachInterrupt(digitalPinToInterrupt(ENC1), updateEncoder, RISING);  // Encoder pin used as interrupt calls updateEncoder function 

  pos = 0; // Initialize encoder position
  prevTime = 0;
  prevError = 0;
  setPoint = 100;
  

}

void loop() {
  
  waitForInput();

  pidLoop();
  
  Serial.print(pos);
  Serial.print("  ");
  Serial.print(error);
  Serial.print("  ");
  Serial.print(derror);
  Serial.print("  ");
  Serial.print(ierror);
  Serial.print("  ");
  Serial.print(u);
  Serial.print("  ");

  
  
  powerMotor(-u);
  Serial.println(testVal);
  delay(200);
    
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
        right(1);
        break;

      case 'r':
        right(-1);
        break;

      case '4':
        right(0);
        break;


      case 'L':
        left(1);
        break;

      case 'l':
        left(-1);
        break;

      case '2':
        left(0);
        break;


      case 'T':
        top(1);
        break;

      case 't':
        top(-1);
        break;

      case '1':
        top(0);
        break;


      case 'D':
        bottom(1);
        break;

      case 'd':
        bottom(-1);
        break;

      case '6':
        bottom(0);
        break;


      case 'F':
        front(1);
        break;

      case 'f':
        front(-1);
        break;

      case '3':
        front(0);
        break;


      case 'B':
        right(1);
        break;

      case 'b':
        right(-1);
        break;

      case '5':
        right(0);
        break;


      case 'i':
        trayCW();
        break;

      case 'o':
        trayCCW();
        break;

      case 'p':
        tray180();
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
      
      default:
        // Code to execute if input is not 1, 2, or 3
        break;
    }
  }
  
}




void trayCW(){
  myStepper.step(50);
  delay(250);
  return;
}

void trayCCW(){
  myStepper.step(-50);
  delay(250);
  return;
}

void tray180(){
  myStepper.step(100);
  delay(250);
  return;
}

void flipShroud(){
  return;
}

void activateShroud(){
  return;
}

void disableShroud(){
  return;
}


void right(int dir){
  disableShroud();
  trayCW();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayCCW();
  }
  else if (dir == -1){
    trayCW();
  }
  else{
    tray180();
  }

  disableShroud();
}



void left(int dir){
  disableShroud();
  trayCCW();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayCCW();
  }
  else if (dir == -1){
    trayCW();
  }
  else{
    tray180();
  }

  disableShroud();
}


void top(int dir){
  disableShroud();
  flipShroud();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayCCW();
  }
  else if (dir == -1){
    trayCW();
  }
  else{
    tray180();
  }

  disableShroud();
}


void bottom(int dir){

  disableShroud();
  activateShroud();
  
  if (dir == 1){
    trayCCW();
  }
  else if (dir == -1){
    trayCW();
  }
  else{
    tray180();
  }

  disableShroud();
}


void front(int dir){

  disableShroud();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayCCW();
  }
  else if (dir == -1){
    trayCW();
  }
  else{
    tray180();
  }

  disableShroud();
}


void back(int dir){

  disableShroud();
  tray180();
  flipShroud();
  activateShroud();
  
  if (dir == 1){
    trayCCW();
  }
  else if (dir == -1){
    trayCW();
  }
  else{
    tray180();
  }

  disableShroud();
}
