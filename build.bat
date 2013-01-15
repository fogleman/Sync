gcc -std=c99 -O3 -c -o _sync.o sync.c
gcc -shared -o _sync.dll _sync.o
del _sync.o
