function sum (a, b) {
	console.log(a+b);
	console.log(a);
	console.log(b);
	return false;
}

sum.apply(this, [1, 2]); 

// Using apply to chain constructors  
Function.prototype.construct = function(aArgs) {
  var fConstructor = this, 
  		fNewConstr = function() { 
  			fConstructor.apply(this, aArgs); 
  		};
  		
  fNewConstr.prototype = fConstructor.prototype;
  return new fNewConstr();
};

function MyConstructor() {
  for (var nProp = 0; nProp < arguments.length; nProp++) {
    this['property' + nProp] = arguments[nProp];
  }
}

var myArray = [4, 'Hello world!', false];
var myInstance = MyConstructor.construct(myArray);

console.log(myInstance.property1);                // alerts 'Hello world!'
console.log(myInstance instanceof MyConstructor); // alerts 'true'
console.log(myInstance.constructor);              // alerts 'MyConstructor'