var restify = require('restify');

function respond(req, res, next){
    res.send('hello' + req.params.name);
}

var server = restify.createServer();
server.get('/hello/:name', respond);
server.head('/hello/:name', respond);

server.listen(3900, function(){
    console.log('%s listening at %s', server.name, server.url);
});
