// sort in reverse order, from new data to old data
// 2016-10-10 K.OHWADA
var payload = msg.payload;
var lines = payload.split("\n");
var len = lines.length;
var text = "";
for (var i=0; i<Math.min((len-1), 40); i++) {
    text += lines[len - i -2] + "<br/>\n";
}
msg.payload = text;
return msg;
