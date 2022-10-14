from time import sleep, perf_counter
import board
import busio
import adafruit_mpu6050
import matplotlib.pyplot as plt

# perf_counter is more precise than time() for dt calculation
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)


accelerationLists = [[],[],[]]
tList = []
totalList = []
dTotalList = []
minList = []
maxList = []
STANDARD_GRAVITY = 9.80665
tolAmt = 2.0

for i in range(3,0,-1):
    print("Starting in : ", i)
    sleep(0.95)

xAcc,yAcc,zAcc = mpu.acceleration
totalDist = (xAcc**2+yAcc**2+zAcc**2)**0.5
dTotalList.append(totalDist)
totalDistGlobal = 9.80665
globalStep = 0
tolAmt = 4.0

while True:
    xAcc,yAcc,zAcc = mpu.acceleration
    totalDist = (abs(xAcc)**2+abs(yAcc)**2+abs(zAcc)**2)**0.5
    if (abs(totalDist - totalDistGlobal) > tolAmt):
        totalDistGlobal = totalDist
        totalList.append(totalDistGlobal)
        if (totalList[len(totalList)-1] - totalList[len(totalList)-2] > 0):
            dTotalList.append(1)
            if (dTotalList[len(dTotalList)-2] != 1):
                minList.append(len(totalList)-1)
        else:
            dTotalList.append(-1)
            if (dTotalList[len(dTotalList)-2] != -1):
                maxList.append(len(totalList) - 1)
    else:
        totalList.append(totalDistGlobal)
        dTotalList.append(dTotalList[len(dTotalList)-1])
    
    curStep = len(maxList)

    if (curStep > globalStep):
        globalStep = curStep
        print(globalStep)

    if (len(totalList) > 50):
        totalList.pop(0)
    if (len(dTotalList) > 50):
        dTotalList.pop(0)
        
"""
#Notable Information
print("Notable Information of intial setup : ")
print("Temperature in Celsius : ",mpu.temperature)
print("Gyro : ", mpu.gyro)
print("Cycle : ", mpu.cycle)
print("Gyro Range : ", mpu.gyro_range)
print("Accelerometer Range : ", mpu.accelerometer_range)
print("Filter Bandwidth : ", mpu.filter_bandwidth)
print("Cycle Rate : ", mpu.cycle_rate)
#Armed and Ready

#Begin Data Aquisition
sleep(0.5)
print("Begin Data Aquisition")
sTime = perf_counter()
cTime = perf_counter()
while (cTime-sTime) < 10.000:
    cTime = perf_counter()
    xAcc,yAcc,zAcc = mpu.acceleration
    tList.append(cTime)
    accelerationLists[0].append(xAcc)
    accelerationLists[1].append(yAcc)
    accelerationLists[2].append(zAcc)
eTime = perf_counter()
print("End Data Aqcuisition")
#End Data Aquisition

#Begin Data Manipulation
sleep(0.5)
print("Begin Data Calculation")
movingAvg = []
totalDistGlobal = STANDARD_GRAVITY
for i in range(len(accelerationLists[0])):
    totalDist = (accelerationLists[0][i]**2+accelerationLists[1][i]**2+accelerationLists[2][i]**2)**0.5
    
    if len(movingAvg) >= 10:
        movingAvg.pop(0)
    movingAvg.append(totalDist)
    totalDist = sum(movingAvg)/len(movingAvg)
    if (i == 0):
        dTotalList.append(totalDist)
    if (abs(totalDist - totalDistGlobal) > tolAmt):
        totalDistGlobal = totalDist
        totalList.append(totalDistGlobal)
        if (totalList[len(totalList) - 1] - totalList[len(totalList)-2] > 0):
            dTotalList.append(1)
            if ( dTotalList[len(dTotalList)-2] != 1):
                minList.append(len(totalList) - 1)
        else:
            dTotalList.append(-1)
            if ( dTotalList[len(dTotalList)-2] != -1):
                maxList.append(len(totalList) - 1)
    else:
        totalList.append(totalDistGlobal)
        dTotalList.append(dTotalList[len(dTotalList)-1])

    
    if (i != 0):
        tList[i] += tList[i-1]-sTime
    else:
        tList[i] -= sTime
print("End Data Calculation")
#End Data Manipulation
    
#Being Output Data
sleep(0.5)
print("Begin Output Data")
print("Total Time Elapsed in Data Aquisition : ",eTime-sTime)
print("Analyzed Steps : ", (len(maxList) + len(minList)/2)/1.5)
print("Plotting TotalAcceleration (Smoothed over 10 data points) vs Time (Seconds) : ")
plt.plot(tList,totalList,label="Line 1")
plt.show()
print("End Output Data")
#End Outpout Data
"""
