#include <MotorWheel.h>
#include <Omni3WD.h>

int p[9];
int RcChannel[9];
long micro_second;
long millis_second,millis_second_before;

#define led 11
#if defined(__AVR_ATmega168) || defined(__AVR_ATmega328__) || defined(__AVR_ATmega328P__)
irqISR(irq1,isr1);
MotorWheel wheel1(9,8,14,15,&irq1);        // Pin9:PWM, Pin8:DIR, Pin14:PhaseA, Pin15:PhaseB
irqISR(irq2,isr2);
MotorWheel wheel2(10,11,16,17,&irq2);    // Pin10:PWM, Pin11:DIR, Pin16:PhaseA, Pin17:PhaseB
irqISR(irq3,isr3);
MotorWheel wheel3(3,2,18,19,&irq3);        // Pin3:PWM, Pin2:DIR, Pin18:PhaseA, Pin19:PhaseB
#elif defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
//irqISR(irq1,isr1);
//MotorWheel wheel1(5,4,3,2,&irq1);  // Motor PWM:Pin5, DIR:Pin4, Encoder A:Pin3, B:Pin2
//irqISR(irq2,isr2);
//MotorWheel wheel2(8,9,18,19,&irq2);    // Motor PWM:Pin8, DIR:Pin9, Encoder A:Pin18, B:Pin19
//irqISR(irq3,isr3);
//MotorWheel wheel3(10,11,20,21,&irq3);    // Motor PWM:Pin10, DIR:Pin11, Encoder A:Pin20, B:Pin21
irqISR(irq1,isr1);
MotorWheel wheel1(5,6,A8,A9,&irq1); // Motor PWM:Pin5, PWM pin 
irqISR(irq2,isr2);
MotorWheel wheel2(7,8,A10,A11,&irq2);    // Motor PWM:Pin7, DIR:Pin8, Encoder A:PinA10, B:PinA11
irqISR(irq3,isr3);
MotorWheel wheel3(9,10,A12,A13,&irq3);    // Motor PWM:Pin9, DIR:Pin10, Encoder A:PinA12, B:PinA13
//irqISR(irq4,isr4);
//MotorWheel wheel4(11,12,A14,A15,&irq4);  // Motor PWM:Pin11, DIR:Pin12, Encoder A:PinA14, B:PinA15
#elif defined(__SAM3X8E__)
irqISR(irq1,isr1);
MotorWheel wheel1(5,6,A8,A9,&irq1);     // Motor PWM:Pin5, DIR:Pin6, Encoder A:PinA8, B:PinA9 
irqISR(irq2,isr2);
MotorWheel wheel2(7,8,A10,A11,&irq2);     // Motor PWM:Pin7, DIR:Pin8, Encoder A:PinA10, B:PinA11
irqISR(irq3,isr3);
MotorWheel wheel3(9,10,A4,A5,&irq3);    // Motor PWM:Pin9, DIR:Pin10, Encoder A:PinDAC0, B:PinDAC1
#endif
Omni3WD Omni(&wheel1,&wheel2,&wheel3);
void setup() 
{
  attachInterrupt(26, RcChannel1, CHANGE);
  attachInterrupt(28, RcChannel2, CHANGE);
  attachInterrupt(30, RcChannel3, CHANGE);
  attachInterrupt(32, RcChannel4, CHANGE);
  Serial.begin(115200);
  pinMode(led,OUTPUT);
#if defined(__AVR_ATmega168__) || defined(__AVR_ATmega328__) || defined(__AVR_ATmega328P__)
  TCCR1B=TCCR1B&0xf8|0x01;    
  TCCR2B=TCCR2B&0xf8|0x01;    
#elif defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
  TCCR2B=TCCR2B&0xf8|0x01;      
  TCCR3B=TCCR3B&0xf8|0x01;       
  TCCR4B=TCCR4B&0xf8|0x01;        
#elif defined(__SAM3X8E__)
#endif
  Omni.PIDEnable(KC,TAUI,TAUD,SAMPLETIME);
  wheel1.PIDEnable(KC,TAUI,TAUD,SAMPLETIME);
  wheel2.PIDEnable(KC,TAUI,TAUD,SAMPLETIME);
  wheel3.PIDEnable(KC,TAUI,TAUD,SAMPLETIME);
}

void loop() 
{
  micro_second = micros();
  millis_second = millis();
  if(millis_second % 10 == 0 && millis_second != millis_second_before)
  {
    millis_second_before = millis_second;
    wheel();
  }
}
