DIR=`pwd`

clang:
	gcc -o app test.c libtestso.h -L${DIR} -ltestso

cpp:
	g++ -o app test.cpp libtestso.h -L${DIR} -ltestso

so: 
	go build -buildmode=c-shared -o libtestso.so main.go

clean:
	rm libtestso.so app libtestso.h

all:	so cpp
