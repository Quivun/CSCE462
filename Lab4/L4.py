import time # sleep, perf_counter
import board
import busio
import adafruit_mpu6050
# perf_counter is more precise than time() for dt calculation
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
# Write a loop to poll each sensor and print its axis values
while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" %(mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" %(mpu.gyro))
    print("")
    sleep(0.1)


