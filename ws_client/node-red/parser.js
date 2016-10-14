// parse the received data in WebSocket node, and convert to csv format
// 2016-10-10 K.OHWADA
var obj = JSON.parse(msg.payload);
if (obj.type == "channels") { 
    var datetime = obj.datetime;
    var channels = obj.payload.channels;
    var len = channels.length;
        var temp = 0;
    var humi = 0;
    var count = 0;
    for (i=0; i<len; i++) {
        var ch = channels[len - i - 1];
        var num = ch.channel;
        if ( num == 0 ) {
                temp = ch.value;
        } else if ( num == 1 ) {
                humi = ch.value;
         } else if ( num == 2 ) {
                count = ch.value;
            }               
    }
        text = datetime + ",";
    text += temp + ",";
    text += humi + ",";
    text += count;
    return { "payload": text };
}
return null;
