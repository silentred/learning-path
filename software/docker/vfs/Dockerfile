FROM alpine:3.5

RUN mkdir /data
ADD ./main /data
RUN dd if=/dev/zero of=/tmp/output.dat bs=500M count=1
WORKDIR /data

ENTRYPOINT ["/data/main"] 