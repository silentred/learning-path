all: lib
	go build main.go

lib:
	gcc -c add.c
	ar q libgb.a add.o

clean:
	rm add.o libgb.a main