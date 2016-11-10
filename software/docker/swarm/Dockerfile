FROM daocloud.io/golang:alpine

RUN mkdir /data
ADD ./main.go /data
WORKDIR /data
RUN go build -o hello .
EXPOSE 9090

ENTRYPOINT ["/data/hello"]  
