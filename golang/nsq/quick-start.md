## สนำร

nsqlookupd

nsqd --lookupd-tcp-address=127.0.0.1:4160 --broadcast-address=127.0.0.1

nsqadmin --lookupd-http-address=127.0.0.1:4161

nsq_to_file --topic=test --output-dir=/tmp --lookupd-http-address=127.0.0.1:4161

curl -d 'hello world 3' 'http://127.0.0.1:4151/put?topic=test'