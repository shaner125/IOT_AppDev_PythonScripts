import grovepi

SOUND = 1
grovepi.pinMode(SOUND, "INPUT")

class SoundSensor():

    def get_sound(self):
        try:
            sensor_value = grovepi.analogRead(SOUND)
            JSONPayload = '{"state":{"reported":{"sound":'+str(sensor_value)+'}}}'
        except IOError:
            print ("Error")
        return JSONPayload
