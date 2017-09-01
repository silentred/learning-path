FROM alpine:3.5

RUN mkdir /data
ADD ./main /data
WORKDIR /data

ENTRYPOINT ["/data/main"] 