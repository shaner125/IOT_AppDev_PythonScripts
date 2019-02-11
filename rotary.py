import grovepi

ROTARY = 2
grovepi.pinMode(ROTARY, "INPUT")

grove_vcc = 5
full_angle = 300
adc_ref = 5

class RotarySensor():

    def get_reading(self):
        try:
            #sensor value from potentiometer
            Rsensor_value = grovepi.analogRead(ROTARY)

            #voltage
            voltage = round((float)(Rsensor_value) * adc_ref / 1023, 2)

            #calculute rotation (0-300)
            degrees = round((voltage * full_angle) / grove_vcc, 2)
            JSONPayload = '{"state":{"reported":{"rotary_angle":'+str(degrees)+'}}}'
        except IOError:
            print ("Error")
        return JSONPayload
