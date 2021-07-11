#include "statemachine.h"
#include "../pwm/pwm.h"
#include <stdio.h>
#include "../ipc/ipc.h"

static state_t state = OFF;
static state_t prev_state = INIT;

static int max_encoder_count = 0;
static int diff1 = 0;
static int prevdiff = 0;
static int diff2 = 0;
static int maxdiff = 0;
static int maxdiffprev = 0;
static int lost_cnt = 0;

void transition_function(int * encoder_count, int * diff1){
    maxdiff = max_encoder_count - *encoder_count;
    
    diff2 = *diff1 - prevdiff;
    prevdiff = *diff1;

        //printf("%d\n", max_encoder_count);
        printf("enc-cnt: %d\t diff1: %d \t diff2: %d \t %d\n", *encoder_count, *diff1, diff2, (maxdiff) );
    
    switch(state) {

        case OFF:
            if (actual_cmd_is("START")) {
                state = ON;
                return;
            }
            break;

        case ON:
            if (actual_cmd_is("STOP")) {
                state = OFF;
                return;
            }

            if (*encoder_count > max_encoder_count) {
                max_encoder_count = *encoder_count;
            }
      
            if (maxdiff + maxdiffprev >= 7) {
                state = SUCKED;
            }
            break;

        case SUCKED: 
            if (actual_cmd_is("STOP")) {
                state = OFF;
            } else if (maxdiff <= 1 && *diff1 == 0) {
                state = LOST;
            }
            break;

        
        case LOST:
            if (actual_cmd_is("STOP")) {
                state = OFF;
            } 
            
            if (lost_cnt > 5) {
                state = OFF;
                lost_cnt = 0;
            }
            break;

        default: printf("default\n"); break;
    }

    maxdiffprev = maxdiff;
}

void output_function() {
    switch(state) {
        case OFF:
            if (prev_state != state) {
                max_encoder_count = 0;
                write_state_to_pipe(state);
                write_pwm(0);
                printf("OFF\n");
            }
            break;
            
        case ON:
            if (prev_state != state) {
                write_state_to_pipe(state);
                write_pwm(100);
                printf("ON\n");
            }

            break;

        case SUCKED:
            if (prev_state != state) {
                write_state_to_pipe(state);
                printf("SUCKED\n");
            }
            break;

        case LOST:
            if (prev_state != state) {
                write_state_to_pipe(state);
                printf("LOST\n");
            }
            lost_cnt++;
            break;
        }
}

void state_machine(int * encoder_count, int * diff1){
    transition_function(encoder_count, diff1);
    output_function();
    prev_state = state;
}

int actual_cmd_is(char * statestr) {
    char state[20];
    strcpy(state, get_actual_cmd());
    strtok(state, "\n");
    return (strcmp(state,statestr) == 0);
}