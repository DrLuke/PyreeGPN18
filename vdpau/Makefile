libpyreevdpau.so: viddecode.o
	gcc -shared -fPIC -lavcodec -lavformat -lswscale -o viddecode.so viddecode.o

vdpau.o: viddecode.h viddecode.c
	gcc -c -fPIC -o viddecode.o viddecode.c -g
