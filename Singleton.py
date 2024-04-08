

import threading
class Singleton(object):
    _instance_lock = threading.Lock()
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