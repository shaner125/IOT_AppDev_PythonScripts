from threading import Thread
import json
import time
import random

class Sensor(Thread):
    
    def __init__(self, observation_type, sampling_rate, active, client):
        self.observation_type = observation_type
        self.default_rate = sampling_rate
        self.sampling_rate = sampling_rate
        self.active = active
        self.client = client
        Thread.__init__(self)

    def get_reading(self):
        return random.randint(1,101)

    def set_rate(self, rate):
        if not (rate <= 2):
            self.sampling_rate = rate
    
    def process(self, json_config):
        self.active = json_config.get("active", False)
        self.sampling_rate = json_config.get("sampling_rate", self.default_rate)
        if self.active:
            print "true"
        
            if not self.isAlive():
                print "lol"
                self.start()
                
    def run(self):
        while self.active:
            dict = {self.observation_type : self.get_reading()}
            json_str = json.dumps(dict)
            self.client.publish("pi/observations/%s" % self.observation_type, json_str, 1)
            print json_str
            time.sleep(self.sampling_rate)
        print 'Stopped publishing %s' % self.observation_type
        Thread.__init__(self)