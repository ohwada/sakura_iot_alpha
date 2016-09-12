# SAKURA IoT
# send data to SAKURA IoT Platform
# 2016-09-01 K.OHWADA

import json
import datetime
import time
import hmac
import hashlib
import requests
import random

#
# SakuraIotSend
#
class SakuraIotSend():
    url = ""
    secret = ""
    module = ""

    def setUrl(self, u):
        print "setUrl " + u
        self.url = u
        
    def setSecret(self, s):
        print "setSecret " + s
        self.secret = s
                    
    def setModule(self, m):
        print "setModule " + m
        self.module = m

    def send(self, data):
        response =""
        try:
            signature = self.createSignature(self.secret, data)
            headers = {"X-Sakura-Signature" : signature}
            requests.post(self.url, data=data, headers=headers)
        except requests.exceptions.HTTPError as e:
            print e
        return response

    def createSignature(self, secret, data):
        return hmac.new( secret.encode("utf-8"), data.encode("utf-8"), hashlib.sha1 ).hexdigest()
            
    def buildJsonChannels(self, channels):
        dt = self.buildDatetimeNow()
        payload = self.buildPayload(channels)
        obj = self.buildObject(dt, self.module, payload)
        return json.dumps(obj)

    def buildDatetimeNow(self):
        return datetime.datetime.now().isoformat()
        
    def buildObject(self, datetime, module, payload):
        obj = {}
        obj["type"] = "channels"
        obj["datetime"] = datetime
        obj["module"] = module
        obj["payload"] = payload
        return obj

    def buildPayload(self, channels):
        payload = {}
        payload["channels"] = channels        
        return payload

    def buildTestChannels(self, ch_min, ch_max, ch_type, val):
        chs = []
        for ch in range(ch_min, ch_max):
            chs.append( self.buildChannel(ch, ch_type, val) )
        return chs

    def buildChannel(self, ch, type, val):
        dict = {}
        dict["channel"] = ch
        dict["type"] = type
        dict["value"] = val
        return dict

# class end
