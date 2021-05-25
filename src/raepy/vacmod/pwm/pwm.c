#include "pwm.h"
#include <stdio.h>

void init_pwm(){
    if(softPwmCreate (OUTPIN, INIT_VAL, RANGE) != 0) {
        printf("softPwmCreat was not successfull \n");
    }
}

void write_pwm(int value) {
    softPwmWrite (OUTPIN, 100-value);
    printf("write-pwm: %d\n", value);
}
