
var util = {};
util.array = {};
util.array.in_array = function (needle, array) {
    for (var i = array.length - 1; i >= 0; i--) {
         if(array[i] == needle)
            return true;
    };

    return false;
}

util.cookie = {};
util.cookie.get = function(key){
    var arrStr = document.cookie.split("; "); 
    var temp;
    for(var i = 0; i < arrStr.length; i++ ){ 
        temp = arrStr[i].split("="); 
        if(temp[0] == key) return unescape(temp[1]); 
    } 
}

util.cookie.getValueFromQueryString = function(query_string, key){
    var list = query_string.split('&');
    for(var i=0; i<list.length; i++){
        var pair = list[i].split('=');
        if(pair[0] == key) return unescape(pair[1]);
    }
}

util.cookie.getUserName = function (argument){
    var query_string_like = util.cookie.get('I');
    return util.cookie.getValueFromQueryString(query_string_like, 'n');
}


//为不支持bind的浏览器兼容(<IE9)
if (!Function.prototype.bind) {
    Function.prototype.bind = function(oThis) {
        if (typeof this !== "function") {
            // closest thing possible to the ECMAScript 5 internal IsCallable function 
            throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
        }
        var aArgs = Array.prototype.slice.call(arguments, 1),
        fToBind = this,
        fNOP = function() {},
        fBound = function() {
            return fToBind.apply(this instanceof fNOP && oThis ? this: oThis, aArgs.concat(Array.prototype.slice.call(arguments)));
        };
        fNOP.prototype = this.prototype;
        fBound.prototype = new fNOP();
        return fBound;
    };
}

/**Parses string formatted as YYYY-MM-DD to a Date object.
  * If the supplied string does not match the format, an
  * invalid Date (value NaN) is returned.
  * @param {string} dateStringInRange format YYYY-MM-DD, with year in
  * range of 0000-9999, inclusive.
  * @return {Date} Date object representing the string.
  */
(function(){
    var D= new Date('2011-06-02T09:34:29+02:00');
    if(!D || +D!== 1307000069000){
        Date.fromISO= function(s){
            var day, tz,
            rx=/^(\d{4}\-\d\d\-\d\d([tT ][\d:\.]*)?)([zZ]|([+\-])(\d\d):(\d\d))?$/,
            p= rx.exec(s) || [];
            if(p[1]){
                day= p[1].split(/\D/);
                for(var i= 0, L= day.length; i<L; i++){
                    day[i]= parseInt(day[i], 10) || 0;
                };
                day[1]-= 1;
                day= new Date(Date.UTC.apply(Date, day));
                if(!day.getDate()) return NaN;
                if(p[5]){
                    tz= (parseInt(p[5], 10)*60);
                    if(p[6]) tz+= parseInt(p[6], 10);
                    if(p[4]== '+') tz*= -1;
                    if(tz) day.setUTCMinutes(day.getUTCMinutes()+ tz);
                }
                return day;
            }
            return NaN;
        }
    }
    else{
        Date.fromISO= function(s){
            return new Date(s);
        }
    }
})()