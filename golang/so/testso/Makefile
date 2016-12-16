DIR=`pwd`

all: so cpp

clang:
    gcc -o app test.c testso.h -L${DIR} -ltestso

cpp:
	g++ -o app test.cpp testso.h -L${DIR} -ltestso

so: 
    go build -buildmode=c-shared -o libtestso.so main.go

clean:
	rm libtestso.so app