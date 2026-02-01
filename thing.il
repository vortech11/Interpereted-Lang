var num1 = 0;
var num2 = 1;
var temp = 0;

var index = 1476;

for (var i = 0; i < index; i = i + 1) {
    //print num1;
    temp = num1 + num2;
    num1 = num2;
    num2 = temp;
}

print num1;