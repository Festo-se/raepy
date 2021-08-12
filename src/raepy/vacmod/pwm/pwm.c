#include "pwm.h"
#include <stdio.h>

void init_pwm(){
    if(softPwmCreate (OUTPIN, INIT_VAL, RANGE) != 0) {
        printf("softPwmCreat was not successfull \n");
    }
}

void write_pwm(int value) {
    softPwmWrite (OUTPIN, 100-value);
    printf("\nwrite-pwm: %d to pin %d\n", value, OUTPIN);
}
