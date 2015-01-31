var http = require('http');

var server = http.createServer(function(req, res){
    res.writeHead(200);
    res.end('Hello HTTP');
});
//console.log(server);
//console.log(server.listen(8088));
server.listen(8088);
