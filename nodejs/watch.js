var fs = require('fs');
var proc = require('process');
var path = require('path');
var walk = function(dir, done) {
    var results = [];
    fs.readdir(dir, function(err, list) {
        if (err) return done(err);
        var i = 0;
        (function next() {
            var file = list[i++];
            if (!file) return done(null, results);
            file = dir + '/' + file;
            fs.stat(file, function(err, stat) {
                if (stat && stat.isDirectory()) {
                    walk(file, function(err, res) {
                        results = results.concat(res);
                        next();
                    });
                } else {
                    results.push(file);
                    next();
                }
            });
        })();
    });
};


var path = process.cwd();
var pidFile = path + '/storage/logs/swoole.pid';

walk('./app', function(err, results){
    for (var i=0; i < results.length ; i++){
        fs.watch(results[i], {}, (eventType, filename) => {
            if (filename) {
                var pid = getPid();
                console.log(pid);
                proc.kill(pid, 'USR1');
            }
        });
    }
});

function getPid (){
    return fs.readFileSync(pidFile);
}