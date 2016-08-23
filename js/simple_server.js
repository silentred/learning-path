var http = require('http');
var url = require('url');

var server = http.createServer(function (req,res) {
    //得到当前请求路径
    var query = url.parse(req.url).query;

    var body = [];

    req.on('data', function(chunk) {
        body.push(chunk);
    }).on('end', function() {
        body = Buffer.concat(body).toString();
        console.log(JSON.stringify({query: query, body: body, url: req.url}));    
    });

    res.end("");
});

server.listen(8083);