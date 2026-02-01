var a = 0;
var b = 1;
var temp = 0;

var index = 1476;

for (var i = 0; i < index; i = i + 1) {
    //print a;
    temp = a + b;
    a = b;
    b = temp;
}

print a;