// handbook
// Type
var boolType = false;
var numberType = 2;
var stringType = "HEllo";
var list = [2, 3, 5];
var list2 = [3, 5, 6];
var Color;
(function (Color) {
    Color[Color["Red"] = 2] = "Red";
    Color[Color["Green"] = 3] = "Green";
    Color[Color["Yellow"] = 4] = "Yellow";
})(Color || (Color = {}));
;
var red = Color.Red;
