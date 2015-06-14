var app = require('http').createServer(handler);
var io = require('socket.io')(app);

var Redis = require('ioredis');
var redis = new Redis('6379', '192.168.1.106');

app.listen(6001, function() {
    console.log('Server is running!');
});

function handler(req, res) {
    res.writeHead(200);
    res.end('');
}

io.on('connection', function(socket) {
    console.log('connected');
});

redis.psubscribe('*', function(err, count) {
    console.log(count);
});

redis.on('pmessage', function(subscribed, channel, message) {
    console.log(subscribed);
    console.log(channel);
    console.log(message);

    message = JSON.parse(message);
    io.emit(channel + ':' + message.event, message.data);
});
