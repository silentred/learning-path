var a = {n: 1}
var b = a;
a.x = a = {n: 2}
console.log(a.x);
console.log(b.x)

var F = function(){};
Object.prototype.a = function(){};
Function.prototype.b = function(){};
var f = new F();
//他这里想问的是f能不能拿到a方法和b方法，我这里知道有坑，我也知道能拿到a，但是我回答的是能拿到a和b，他说不对，然后就过了，我觉得这里是我表达不对，因为在读Backbone源码的时候，我使用过f.constructor可以同时拿到a和b，结果他以为我认为直接通过f拿

//判断IE9以上
//if(  document.addEventListener  ){
//	alert("you got IE9 or greater");
//}
//IE8绑定change事件
//$('#commentTextarea').bind('propertychange input paste', comment.limitWordEvent);

let each = Array.prototype.forEach;
