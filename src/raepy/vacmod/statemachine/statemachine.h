#ifndef STATEMACHINE_H
#define STATEMACHINE_H
typedef enum {INIT, OFF, ON, SUCKED, LOST} state_t;

static int max_encoder_count;

void state_machine(int * encoder_count, int * diff1);
void output_function();
void transition_function(int * encoder_count, int * diff1);
int actual_cmd_is(char * statestr);

#endif