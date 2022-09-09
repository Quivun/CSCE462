import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH) 

rgb1Pins = {'ledR' : 22, 'ledG' : 27, 'ledB' : 17}
rgb2Pins = {'ledR' : 25, 'ledG' : 24, 'ledB' : 23}
timerPins = {'timerA' : 16, 'timerB' : 12, 'timerC' : 13, 'timerD' : 19, 'timerE' : 26, 'timerF' : 20, 'timerG' : 21, 'timerDP' : 6}
btn = 18

def setup():
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

    for i in rgb1Pins:
        GPIO.setup(rgb1Pins[i], GPIO.OUT)
        GPIO.output(rgb1Pins[i],GPIO.HIGH)

    for i in rgb2Pins:
        GPIO.setup(rgb2Pins[i], GPIO.OUT)
        GPIO.output(rgb2Pins[i],GPIO.HIGH)

    for i in timerPins:
        GPIO.setup(timerPins[i], GPIO.OUT)
        GPIO.output(timerPins[i],GPIO.HIGH)

def red(rgbDict):
    GPIO.output(rgbDict['ledR'],GPIO.LOW)
    GPIO.output(rgbDict['ledG'],GPIO.HIGH)
    GPIO.output(rgbDict['ledB'],GPIO.HIGH)

def green(rgbDict):
    GPIO.output(rgbDict['ledR'],GPIO.HIGH)
    GPIO.output(rgbDict['ledG'],GPIO.LOW)
    GPIO.output(rgbDict['ledB'],GPIO.HIGH)

def blue(rgbDict):
    GPIO.output(rgbDict['ledR'],GPIO.HIGH)
    GPIO.output(rgbDict['ledG'],GPIO.HIGH)
    GPIO.output(rgbDict['ledB'],GPIO.LOW)

# A7 B6 C4 D2 E1 F9 G10 DP5 
# Ignore the period DP, Set inactive

#set pins as outputs
#GPIO.setup(pinNum,GPIO.OUT)
#GPIO.output(pinNum,GPIO.LOW) // Active
#GPIO.output(pinNum,GPIO.HIGH) // Inactive

def btnUnpressed():
    while True:
        if GPIO.input(btn) == GPIO.HIGH:
            break
    btnPressed()

def btnPressed(): # Naive Segmented method Linear
    GPIO.output(rgb2Pins['ledG'],GPIO.HIGH)
    
    for i in range(0,3):
        GPIO.output(rgb2Pins['ledB'],GPIO.LOW)
        sleep(.5)
        GPIO.output(rgb2Pins['ledB'],GPIO.HIGH)
        sleep(.5)

    GPIO.output(rgb2Pins['ledR'],GPIO.LOW)
    GPIO.output(rgb1Pins['ledG'],GPIO.LOW)
    countdown()
    GPIO.output(rgb1Pins)
    
    btnUnpressed()


def main():
    setup()
    GPIO.output(rgb2Pins['ledG'],GPIO.LOW) # LED 2 Stays green
    btnUnpressed()

if __name__ == "__main__":
    main()
    GPIO.cleanup()