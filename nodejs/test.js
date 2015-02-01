var assert = require('assert');

//assert.fail(false, true, 'error', '=');

assert(true);
assert.ok(1);
assert.notEqual(1, 2, 'they are equal');

var b = new Buffer(12);
b = new Buffer([1,2,3,4]);
b = new Buffer('string', 'utf8');
b.write('123');

console.log(b);

var fs = require('fs')
  , sys = require('sys');

fs.readFile('A.txt', function(error, data) {
  sys.puts("oh, look at all my money: "+data);
});

fs.writeFile('B.txt', '...', function() {
  sys.puts("can't wait to hear back from her!");
});

/*var dns = require('dns');
dns.resolve4('www.baidu.com', function (err, addresses) {
    if (err) throw err;
    console.log('addresses: ' + JSON.stringify(addresses)); 
});*/

//console.log(globals);
//console.log(process);

/*
var crypto = require('crypto');
//var fs = require('fs'); 
var zlib = require('zlib'); 
var password = new Buffer(process.env.PASS || 'password'); 
var encryptStream = crypto.createCipher('aes-256-cbc', password); 
var gzip = zlib.createGzip(); 
var readStream = fs.createReadStream(__filename); // current file 
var writeStream = fs.createWriteStream(__dirname + '/out.gz'); 
readStream // reads current file 
.pipe(encryptStream) // encrypts 
.pipe(gzip) // compresses 
.pipe(writeStream) // writes to out file 
.on('finish', function () { // all done 
	console.log('done'); 
});*/


/*var decryptStream = crypto.createDecipher('aes-256-cbc', password);
var gunzip = zlib.createGunzip();
var readStream = fs.createReadStream(__dirname + '/out.gz');
readStream // reads current file 
.pipe(gunzip) // uncompresses 
.pipe(decryptStream) // decrypts 
.pipe(process.stdout) // writes to terminal 
.on('finish', function () { // finished 
	console.log('done'); 
});
*/










