double cos_theta;
double sin_theta;
double pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489;
double degree;
double sp;
double v1;
double v2;
double v3;
double wp;

void wheel()
{ 
  if (RcChannel[1] == 0 || RcChannel[2] == 0)
  {
    sp = 0;
    degree = 0;
  }
  else
  {
    sp = map(RcChannel[2],1100,1900,-200,200);
    degree = map(RcChannel[1],1100,1900,-90,90);
  }
  //Serial.println(sp);
  Serial.println(degree);
  wp = 0;
  cos_theta = cos(pi/180*degree);
  sin_theta = sin(pi/180*degree);
  v1 = sp*sin_theta + wp*(0.12);
  v2 = -(sp*sin_theta/2) + (0.867)*sp*cos_theta + wp*(0.12);
  v3 = -(sp*sin_theta/2) - (0.867)*sp*cos_theta + wp*(0.12);
  if(v1 > 0)
  {
    wheel1.setSpeedMMPS(v1,DIR_ADVANCE);
    wheel1.PIDRegulate(); 
  }
  else
  {
    wheel1.setSpeedMMPS(-v1,DIR_BACKOFF);
    wheel1.PIDRegulate(); 
  }
    if(v2 > 0)
  {
    wheel2.setSpeedMMPS(v2,DIR_ADVANCE);
    wheel2.PIDRegulate(); 
  }
  else
  {
    wheel2.setSpeedMMPS(-v2,DIR_BACKOFF);
    wheel2.PIDRegulate(); 
  }
    if(v3 > 0)
  {
    wheel3.setSpeedMMPS(v3,DIR_ADVANCE);
    wheel3.PIDRegulate(); 
  }
  else
  {
    wheel3.setSpeedMMPS(-v3,DIR_BACKOFF);
    wheel3.PIDRegulate(); 
  }
}
