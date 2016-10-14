// select the latest 100 of data, and convert the graph format
// 2016-10-10 K.OHWADA
var payload = msg.payload;
var lines = payload.split("\n");
var len = lines.length;
var start = len - 100;
if (start<0) {
    start = 0;
}   
var text = [];
for (var i=start; i<(len-1); i++) {
    var line = lines[i];
    var cols = line.split(",");
    var obj = {};
    obj.datetime = new Date(cols[0]);
    obj.temperature = parseFloat(cols[1]);
//  obj.humidity = parseFloat(cols[2]);
//  obj.count = parseInt(cols[3]);  
    text.push(obj);
}
msg.payload = text;
return msg;