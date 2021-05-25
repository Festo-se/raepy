#include "encoder.h"
#include <pthread.h>
#include <wiringPi.h>
#include <errno.h>
#include <stdio.h>


pthread_t id;

void interrupt_routine (void) { counter++; };

void * counter_reset(void * callback) {
    void (*cb)(int) = callback;

    while(1) {
        delay(200);
        cb(&counter);
        counter = 0;
    }
}

int init_encoder(void (*cb)(void)) {

    wiringPiSetup();
    pullUpDnControl(PIN,PUD_UP);
    if(wiringPiISR (PIN, INT_EDGE_FALLING, &interrupt_routine) < 0 ){
        fprintf (stderr, "Unable to setup ISR: %d\n", strerror (errno)) ;
        return 1 ;
    }
    pthread_create(&id, NULL, counter_reset, (void*) cb);
}