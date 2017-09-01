build:
	CGO_ENABLED=0 go build -o main main.go
	docker build -t vfstest .

clean:
	rm main
	docker rmi vfstest
