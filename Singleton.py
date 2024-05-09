

import threading
class Singleton(object):
    _instance_lock = threading.Lock()
    bi_data = []
    config = {}
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance
    def set(self, key, value):
        self.config[key] = value

    def get(self, key):
        return self.config.get(key)

    def getConfig(self):
        return self.config

    def setBiData(self,data):
        self.bi_data = data

    def getBiData(self):
        return self.bi_data

    def clearBiData(self):
        self.bi_data.clear()