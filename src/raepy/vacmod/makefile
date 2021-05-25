vacmod: main.o encoder.o pwm.o statemachine.o ipc.o
	gcc -o vacmod main.o encoder.o pwm.o statemachine.o ipc.o -pthread -lwiringPi -lm -lrt -lcrypt

main.o: main.c
	gcc -c main.c

encoder.o: encoder/encoder.c
	gcc -c encoder/encoder.c

pwm.o: pwm/pwm.c
	gcc -c pwm/pwm.c

statemachine.o: statemachine/statemachine.c
	gcc -c statemachine/statemachine.c

ipc.o: ipc/ipc.c
	gcc -c ipc/ipc.c