var http = require('http');
var fs = require('fs');
var url = require('url');
var server = http.createServer(function (req,res) {
	//得到当前请求路径
	var url_path = url.parse(req.url).pathname; 
	var cur_dir = __dirname;
	
	//首页以'/'结尾，则判断是否存在/index.html
	if(url_path=='/' && fs.existsSync(cur_dir+url_path+'index.html')){
		url_path += 'index.html';
	}
	
	//读取文件内容，返回。若出错，则返回404
	fs.readFile(cur_dir+url_path, function (err, data) {
		if (err) {
			res.writeHead(404);
			res.end('404 not found');
		}
		res.end(data);
	});
    
});
server.listen(80);

console.log('Listening on port 80.');