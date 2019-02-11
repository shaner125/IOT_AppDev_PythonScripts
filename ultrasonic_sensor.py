import grovepi

ULTRA = 2
grovepi.pinMode(ULTRA, "INPUT")

class UltraSensor():

    def get_reading(self):
        try:
            sensor_value = grovepi.ultrasonicRead(ULTRA)
            JSONPayload = '{"state":{"reported":{"ultra":'+str(sensor_value)+'}}}'
        except IOError:
            print ("Error")
        return JSONPayload
