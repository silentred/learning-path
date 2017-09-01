build:
	CGO_ENABLED=0 go build -o main main.go
	docker build -t vsftest .

clean:
	rm main
	docker rmi vsftest
