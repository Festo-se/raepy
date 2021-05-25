#ifndef ENCODER_H_
#define ENCODER_H_

#define PIN 1
#define DELAY 200

static volatile int counter = 0;

void interrupt_routine(void);
void * counter_reset(void * callback);
int init_encoder(void (* result_callback)(void));

#endif