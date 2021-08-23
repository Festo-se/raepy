
#include "encoder/encoder.h"
#include "pwm/pwm.h"
#include "ipc/ipc.h"
#include "statemachine/statemachine.h"

#include <stdio.h>
#include <wiringPi.h>

int encoder_count = 0;
int prev_count = 0;
int diff1 = 0;

void loop() {
    diff1 = encoder_count - prev_count;
    state_machine(&encoder_count, &diff1);
    prev_count = encoder_count;
}

void encoder_result(int * result) {
    //printf("result: %d\n", *result);
    encoder_count = * result;
    //stateMachine(&encoder_count);
    loop(); // called every 200 ms
}


int main(void) {
    init_encoder(encoder_result);
    init_pwm();
    init_ipc();
    while(1) {
        delay(100);
    }
    printf("End");
}