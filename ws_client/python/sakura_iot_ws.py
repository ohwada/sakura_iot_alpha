#!/usr/bin/env python

# SAKURA IoT - WebSocket Client
# parse the mesage from SAKURA IoT Platform
# 2016-06-20 K.OHWADA

import websocket
import thread
import sys
import json
import datetime
import time

TOKEN = "your_token"
URL = "wss://secure.sakura.ad.jp/iot-alpha/ws/" + TOKEN

g_cnt = 0

#
# SakuraIot
#
class SakuraIot():
    ch_min = 3
    ch_max = 6
    ch_type = "I"
    module = ""
    isFirst = True
            
    def setModule(self, m):
        self.module = m

    def buildJson(self, val):
        if not self.module:
            return ''
        obj = self.buildObject(val)
        text = json.dumps(obj)
        return text

    def buildObject(self, val):
        dt = datetime.datetime.now().isoformat()
        obj = {}
        obj["type"] = "channels"
        obj["datetime"] = dt
        obj["module"] = self.module
        obj["payload"] = self.buildPayload(val)
        return obj

    def buildPayload(self, val):
        payload = {}
        payload["channels"] = self.buildChannels(val)        
        return payload

    def buildChannels(self, val):
        chs = []
        for ch in range(self.ch_min, self.ch_max):
            chs.append( self.buildChannel(ch, val) )
        return chs

    def buildChannel(self, ch, val):
        dict = {}
        dict["channel"] = ch
        dict["type"] = self.ch_type
        dict["value"] = val
        return dict

    def printRecv(self, message):
        obj = json.loads(message)
        if obj["type"] is None:
            print message
            return
        str_type = obj["type"] 
        if str_type == "keepalive":
            self.printKeepalive(obj)
            return
        elif str_type == "channels":  
            self.printChannels(obj)                          

    def printKeepalive(self, obj):
        print "type: " + obj["type"] 
        print "datetime: " + obj["datetime"]

    def printChannels(self, obj):
        if self.isFirst:
            self.setModule( obj["module"] )
            self.isFirst = False
        print "type: " + obj["type"]
        print "datetime: " + obj["datetime"]
        print "module: " + obj["module"]
        channels = obj["payload"]["channels"]
        for ch in channels:
            print "channel: " + str(ch["channel"]) \
                + " type: " + ch["type"] \
                + " value: " + str(ch["value"])

# class end

# === main ===           
iot = SakuraIot()

#
# on_message
#                           
def on_message(ws, message):
#    print "debug: on_message"
#    print message
    print ""
    iot.printRecv(message)

#
# on_error
# 
def on_error(ws, error):
    print "debug: on_error"
    print error

#
# on_close
# 
def on_close(ws):
    print "debug: on_close"

#
# on_open
# 
def on_open(ws):
    print "debug: on_open"
    def run(*args):
        while(True):
#            send_message(ws)
            time.sleep(1)

    thread.start_new_thread(run, ())

#
# send_message
#
def send_message(ws):
    global g_cnt
    text = iot.buildJson(g_cnt)
    if text:
        g_cnt += 1
        print ""
        print "debug: sending:"
        print text
        ws.send(text)

#
# --- main ---
#         
if __name__ == "__main__":
#    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(URL,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
