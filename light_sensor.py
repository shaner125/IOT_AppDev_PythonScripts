import grovepi

LIGHT = 0
grovepi.pinMode(LIGHT, "INPUT")

class LightSensor():

    def get_reading(self):
        try:
            sensor_value = grovepi.analogRead(LIGHT)
            JSONPayload = '{"state":{"reported":{"light":'+str(sensor_value)+'}}}'
        except IOError:
            print ("Error")
        return JSONPayload
