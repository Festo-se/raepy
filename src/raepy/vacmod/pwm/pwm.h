#ifndef PWM_H
#define PWM_H

#include <softPwm.h>

#define OUTPIN 0
#define INIT_VAL 100
#define RANGE 100

void write_pwm(int value);
void init_pwm();

#endif