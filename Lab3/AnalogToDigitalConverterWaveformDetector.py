from math import sin, pi, abs
import time
import wave
from adafruit_mcp3xxx.analog_in import AnalogIn

# import os
import busio
import digitalio
import board
# import adafruit_mcp4725
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO

"""
dac.raw_value = [0,4095]
Channel.value = [0,(2^16)-1] Integer
Channel.voltage = [0,3.3 (Or 5.0 maybe?)] Float 
"""

# Setup
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)  # create spi bus
cs = digitalio.DigitalInOut(board.D22)  # create chip select
mcp = MCP.MCP3008(spi, cs)  # create mcp object
channel = AnalogIn(mcp, MCP.P0)  # create analog input channel on pin 0

# Hardware dependent values
rPSInt = 2000  # Integer reads per second
iInt = 1.0  # Float time before next check
tolInt = 5000  # Integer tolerance of RAW value [0,65535]
tolDx = 500  # Integer tolerance of slope value [0,65535]


def s1DataGens2DataClean():
    dxList, maxList, minList, xList = (
        [],
        [],
        [],
        [],
    )  # dx is to determine slope direction to populate maxList and minList (That will also provide the returned frequency and a sample of a wave). xList are the raw values taken in by reads from the ADC
    curVal, gloVal = (
        0,
        0,
    )  # curVal is an instance of ADC's read value while gloVal maintains consistency within a threshold tolerance.
    curVal = channel.value
    xList.append(curVal)
    curVal = channel.value
    xList.append(curVal)
    dxList.append(1 if xList[1] > xList[0] else -1)
    gloVal = curVal
    sTime = time.clock()
    for i in range(
        0, rPSInt, 1
    ):  # Cycle a tested amount that is guaranteed 1 second real time for as many times we can read the channel value and populate each list accordingly.
        curVal = channel.value
        if (abs(curVal - gloVal) > tolInt):
            gloVal = curVal
            xList.append(gloVal)
            if xList[len(xList) - 1] - xList[len(xList) - 2] > 0:
                dxList.append(1)
                if dxList[len(dxList) - 2] != 1:
                    minList.append(len(xList) - 1)
            else:
                dxList.append(-1)
                if dxList[len(dxList) - 2] != -1:
                    maxList.append(len(xList) - 1)
        else:
            xList.append(gloVal)
            dxList.append(dxList[len(dxList) - 1])
    eTime = time.clock()
    print(eTime-sTime, " is the Elapsed time it took for ", rPSInt, " value reads")
    if (
        maxList[1] > minList[1]
    ):  # Determines if the xList started off measuring a min or a max and adjusting output accordingly.
        return (len(maxList) + len(minList)) / 2, xList[maxList[1] : minList[2] + 1]
    else:
        return (len(maxList) + len(minList)) / 2, xList[maxList[1] : minList[1] + 1]


def s3Eval(waveArr):
    # waveArr is a subsection of the array containing a the max and min of the single waveform from the 25% and 75% marker.
    dx1 = waveArr[int(len(waveArr) * 0.25) - 1] - waveArr[0]
    if dx1 == 0:
        return "Square"
    dx2 = waveArr[int(len(waveArr) * 0.75) - 1] - waveArr[int(len(waveArr) * 0.25) - 1]
    if abs(dx1 - dx2 < tolDx):
        return "Triangle"
    else:
        return "Sine"  # dx3 = waveArr[int(len(waveArr)-1)] - waveArr[int(len(waveArr)*0.75 - 1)]


def main():
    # The scope of accuracy applies from 1 hz to 1750 hz assumed.
    curWave = ""
    globalWave = "NULL"
    while True:
        freqInt, waveArr = s1DataGens2DataClean()
        print("Frequency : ", freqInt)
        curWave = s3Eval(waveArr)
        if globalWave != curWave:
            globalWave = curWave
            # Might implement a double check before outputting new Waveform official. Why? Because the waveform and frequency may be changed mid read.
            print("New Waveform detected : ", globalWave)
        time.sleep(iInt)


if __name__ == "__main__":
    main()
