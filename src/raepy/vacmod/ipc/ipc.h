#ifndef IPC_H
#define IPC_H

#include <pthread.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include "../statemachine/statemachine.h"

int fd;

// FIFO file path
char * statefifo;
char * cmdfifo;

char actual_cmd[10];
char cmd_buffer[10];

void * read_cmd_from_pipe();
void write_state_to_pipe(state_t state);
void init_ipc();
char * get_actual_cmd();

#endif