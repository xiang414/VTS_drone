
void RcChannel1() 
{
  if(micro_second - p[1] < 2000)
  {
    RcChannel[1] = micro_second - p[1];
  }
  p[1] = micro_second;
}

void RcChannel2() 
{
  if(micro_second - p[2] < 2000)
  {
    RcChannel[2] = micro_second - p[2];
  }
  p[2] = micro_second;
}

void RcChannel3() 
{
  if(micro_second - p[3] < 2000)
  {
    RcChannel[3] = micro_second - p[3];
  }
  p[3] = micro_second;
}

void RcChannel4() 
{
  if(micro_second - p[4] < 2000)
  {
    RcChannel[4] = micro_second - p[4];
  }
  p[4] = micro_second;
}

void RcChannel5() 
{
  if(micro_second - p[5] < 2000)
  {
    RcChannel[5] = micro_second - p[5];
  }
  p[5] = micro_second;
}

void RcChannel6() 
{
  if(micro_second - p[6] < 2000)
  {
    RcChannel[6] = micro_second - p[6];
  }
  p[6] = micro_second;
}

void RcChannel7() 
{
  if(micro_second - p[7] < 2000)
  {
    RcChannel[7] = micro_second - p[7];
  }
  p[7] = micro_second;
}

void RcChannel8() 
{
  if(micro_second - p[8] < 2000)
  {
    RcChannel[8] = micro_second - p[8];
  }
  p[8] = micro_second;
}
