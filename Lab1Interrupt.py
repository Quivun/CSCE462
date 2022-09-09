import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

rgb1Pins = {'ledR' : 22, 'ledG' : 27, 'ledB' : 17}
rgb2Pins = {'ledR' : 25, 'ledG' : 24, 'ledB' : 23}
timerPins = {'A' : 16, 'B' : 12, 'C' : 13, 'D' : 19, 'E' : 26, 'F' : 20, 'G' : 21, 'DP' : 6}
btn = 18

def setup():
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

    for i in rgb1Pins:
        GPIO.setup(rgb1Pins[i], GPIO.OUT)
        GPIO.output(rgb1Pins[i],GPIO.HIGH)

    for i in rgb2Pins:
        GPIO.setup(rgb2Pins[i], GPIO.OUT)
        GPIO.output(rgb2Pins[i],GPIO.HIGH)

    for i in timerPins:
        GPIO.setup(timerPins[i], GPIO.OUT)
        GPIO.output(timerPins[i],GPIO.HIGH)

# A7 B6 C4 D2 E1 F9 G10 DP5 
# Ignore the period DP, Set inactive

#set pins as outputs
#GPIO.setup(pinNum,GPIO.OUT)
#GPIO.output(pinNum,GPIO.LOW) // Active
#GPIO.output(pinNum,GPIO.HIGH) // Inactive

def callbackDetect(input_pin): 
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
    GPIO.output(rgb1Pins['ledR'],GPIO.HIGH)

    countdown()

    GPIO.output(rgb2Pins['ledR'],GPIO.HIGH)
    GPIO.output(rgb1Pins['ledR'],GPIO.LOW)
    GPIO.output(rgb2Pins['ledG'],GPIO.LOW)

    for i in timerPins:
        GPIO.output(timerPins[i],GPIO.HIGH)
    
    sleep(8)

def countdown():
    GPIO.output(timerPins['A'],GPIO.LOW)
    GPIO.output(timerPins['B'],GPIO.LOW)
    GPIO.output(timerPins['C'],GPIO.LOW)
    GPIO.output(timerPins['D'],GPIO.LOW)
    GPIO.output(timerPins['F'],GPIO.LOW)
    GPIO.output(timerPins['G'],GPIO.LOW)
    sleep(1)
    GPIO.output(timerPins['E'],GPIO.LOW)
    sleep(1)
    GPIO.output(timerPins['D'],GPIO.HIGH)
    GPIO.output(timerPins['E'],GPIO.HIGH)
    GPIO.output(timerPins['F'],GPIO.HIGH)
    GPIO.output(timerPins['G'],GPIO.HIGH)
    sleep(1)
    GPIO.output(timerPins['B'],GPIO.HIGH)
    GPIO.output(timerPins['D'],GPIO.LOW)
    GPIO.output(timerPins['E'],GPIO.LOW)
    GPIO.output(timerPins['F'],GPIO.LOW)
    GPIO.output(timerPins['G'],GPIO.LOW)
    sleep(1)
    GPIO.output(timerPins['E'],GPIO.HIGH)
    sleep(1)
    GPIO.output(timerPins['A'],GPIO.HIGH)
    GPIO.output(timerPins['B'],GPIO.LOW)
    GPIO.output(timerPins['D'],GPIO.HIGH)
    
    GPIO.output(rgb1Pins['ledG'],GPIO.HIGH)

    for i in range(0,2):
        GPIO.output(rgb1Pins['ledB'],GPIO.LOW)
        sleep(.25)
        GPIO.output(rgb1Pins['ledB'],GPIO.HIGH)
        sleep(.25)    

    GPIO.output(timerPins['A'],GPIO.LOW)
    GPIO.output(timerPins['D'],GPIO.LOW)
    GPIO.output(timerPins['F'],GPIO.HIGH)

    for i in range(0,2):
        GPIO.output(rgb1Pins['ledB'],GPIO.LOW)
        sleep(.25)
        GPIO.output(rgb1Pins['ledB'],GPIO.HIGH)
        sleep(.25)

    GPIO.output(timerPins['C'],GPIO.HIGH)
    GPIO.output(timerPins['E'],GPIO.LOW)

    for i in range(0,2):
        GPIO.output(rgb1Pins['ledB'],GPIO.LOW)
        sleep(.25)
        GPIO.output(rgb1Pins['ledB'],GPIO.HIGH)
        sleep(.25)

    GPIO.output(timerPins['A'],GPIO.HIGH)
    GPIO.output(timerPins['C'],GPIO.LOW)
    GPIO.output(timerPins['D'],GPIO.HIGH)
    GPIO.output(timerPins['E'],GPIO.HIGH)
    GPIO.output(timerPins['G'],GPIO.HIGH)

    for i in range(0,2):
        GPIO.output(rgb1Pins['ledB'],GPIO.LOW)
        sleep(.25)
        GPIO.output(rgb1Pins['ledB'],GPIO.HIGH)
        sleep(.25)
    
    GPIO.output(timerPins['A'],GPIO.LOW)
    GPIO.output(timerPins['D'],GPIO.LOW)
    GPIO.output(timerPins['E'],GPIO.LOW)
    GPIO.output(timerPins['F'],GPIO.LOW)

def main():
    setup()
    GPIO.output(rgb2Pins['ledG'],GPIO.LOW) # LED 2 Stays green
    GPIO.add_event_detect(btn, GPIO.RISING, callback=callbackDetect)

if __name__ == "__main__":
    main()
    GPIO.cleanup()