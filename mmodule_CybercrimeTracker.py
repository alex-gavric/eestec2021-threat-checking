from Module import Module
from jsonRW import read_json_file

import time
import pandas as pd
import redis

rds = redis.Redis(host='localhost', port=6379, db=0)

class CybercrimeTracker(Module):
    
    def __init__(self):
        path = './data/CYBERCRiME.txt'
        name = self.__class__.__name__
        file1 = open(path, 'r')
        Lines = file1.readlines()
        result = self.Decode(rds.get(name))
        if result != "uploaded":
            for row in Lines:
                rds.set(name + ":" + row, "detected")
            rds.set(name, "uploaded")

    def send_hash(self, hash_str):
        return self.send_url(hash_str)

    def send_file(self, location_of_file):
        return {"type":"error","message":"not implemented", 'name' : self.__class__.__name__ }
                
    def send_url(self, string):
        name = self.__class__.__name__
        result = self.Decode(rds.get(name + ":" + string + '\n'))
        if result != "detected":
            result = "undetected"
        return {"type":"error","message":result, 'name' : self.__class__.__name__ }
    
    def send_ip(self, string):
        return self.send_url(string)
    
    def get_data(self,data):        
        ret = {'type':'report', 'name' : self.__class__.__name__ }
        ret['malicious'] = data.get('suspicious', 0) + data.get('malicious', 0)
        ret['undetected'] = data.get('harmless', 0) + data.get('undetected', 0)
        ret["message"] = "Malicious: " + ret['malicious'] + ", Undetected: " + ret['undetected']
        return ret
    
    def Decode(self, bytesStr):
        if bytesStr is not None:
            return bytesStr.decode("utf-8")
        else:
            return None

    
def get_obj(): return CybercrimeTracker()

#v = DanMe_Uk()
