#include "ipc.h"


// FIFO file path
char * statefifo = "/tmp/vacmodstate";
char * cmdfifo = "/tmp/vacmodcmd";

pthread_t idipc;


void init_ipc() {
    mkfifo(statefifo, 0666);
    mkfifo(cmdfifo, 0666);
    pthread_create(&idipc, NULL, read_cmd_from_pipe, NULL);
}

char * get_actual_cmd() {
    strcpy(cmd_buffer, actual_cmd);
    strcpy(actual_cmd,"");
    return cmd_buffer;
}

void * read_cmd_from_pipe(){
    while(1) {
        fd = open(cmdfifo, O_RDONLY);
        read(fd, actual_cmd, sizeof(actual_cmd));
        close(fd);
    }
}

void write_state_to_pipe(state_t state){
    char statestr[10];
    switch(state) {
        case OFF:
            strcpy(statestr, "OFF");
            break;
        case ON:
            strcpy(statestr, "ON");
            break;
        case SUCKED:
            strcpy(statestr, "SUCKED");
            break;
        case LOST:
            strcpy(statestr, "LOST");
            break;
    }
    
    fd = open(statefifo, O_CREAT|O_WRONLY);
    write(fd, statestr, strlen(statestr)+1);
    close(fd);
}