FROM daocloud.io/library/golang:latest

RUN mkdir /data
ADD ./main.go /data
WORKDIR /data
RUN go build -o hello .
EXPOSE 9090

CMD ["/data/hello"] 