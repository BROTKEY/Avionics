import threading
import board
import adafruit_bmp3xx
import adafruit_bno055
import picamera
import socket
import time
import RPi.GPIO as GPIO
import time

RUN = True
TARGETIP = "192.168.43.59"

relaisOne = 17
relaiTwo = 27
i2c = board.I2C()
bno = adafruit_bno055.BNO055_I2C(i2c)


def BMP388():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    i2c = board.I2C()
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    with open("BMP388_Logs.csv", "w") as myfile:
        myfile.write("altitude,pressure,temperature\n")
        while RUN:
            data = "{0:0>9.4f},{1:0>9.4f},{2:0>8.4f}".format(
                bmp.altitude, bmp.pressure, bmp.temperature)
            sock.sendto(bytes(data, "utf-8"), (TARGETIP, 691))
            myfile.write(data+"\n")


def BNO055Euler():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with open("BNO055Euler_Logs.csv", "w") as myfile:
        myfile.write("x,y,z\n")
        while RUN:
            x, y, z = bno.euler
            if type(x) == float and type(y) == float and type(y) == float:
                if (x < 360 and y < 360 and z < 360) and (x > -360 and y > -360 and z > -360):
                    data = "{0:0<9.4f},{1:0<9.4f},{2:0<8.4f}".format(x, y, z)
                    sock.sendto(bytes(data, "utf-8"), (TARGETIP, 692))
                    myfile.write(data+"\n")

def BNO055Accel():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with open("BNO055Accel_Logs.csv", "w") as myfile:
        myfile.write("x,y,z\n")
        while RUN:
            x, y, z = bno.acceleration
            if type(x) == float and type(y) == float and type(y) == float:
                data = "{0:0<9.4f},{1:0<9.4f},{2:0<8.4f}".format(x, y, -z)
                sock.sendto(bytes(data, "utf-8"), (TARGETIP, 693))
                myfile.write(data+"\n")                    


def NoLoopGuidance():
    start = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start.bind(("0.0.0.0", 694))
    start.recvfrom(6)
    print("launch")
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(relaisOne, GPIO.OUT)
    GPIO.setup(relaiTwo, GPIO.OUT)
    GPIO.output(relaisOne, GPIO.LOW)
    GPIO.output(relaiTwo, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(relaisOne, GPIO.HIGH)
    print("Relay 1 click")
    time.sleep(0.2)
    GPIO.output(relaisOne, GPIO.LOW)
    time.sleep(2.1)
    GPIO.output(relaiTwo, GPIO.HIGH)
    print("Relay 2 click")
    time.sleep(0.2)
    GPIO.output(relaiTwo, GPIO.LOW)
    GPIO.cleanup()


def camera():
    camera = picamera.PiCamera()
    camera.start_recording('flight.h264')
    while RUN:
        pass
    camera.stop_recording()


BMP388Thread = threading.Thread(target=BMP388)
BMP388Thread.start()
BNO055ThreadGyro = threading.Thread(target=BNO055Euler)
BNO055ThreadGyro.start()
BNO055ThreadAccel = threading.Thread(target=BNO055Accel)
BNO055ThreadAccel.start()
LaunchThread = threading.Thread(target=NoLoopGuidance)
LaunchThread.start()
cameraThread = threading.Thread(target=camera)
cameraThread.start()

print("Startup succesfull")
input()
RUN = False
BMP388Thread.join()
print("Stopped BMP388")
BNO055ThreadGyro.join()
print("Stopped BNO55Gyro")
BNO055ThreadAccel.join()
print("Stopped BNO055Accel")
cameraThread.join()
print("Stopped Camera")
LaunchThread.join()
print("Stopped Launch")
