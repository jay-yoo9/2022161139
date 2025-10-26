import threading
import serial
import time
import RPi.GPIO as GPIO

PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 24
BIN2 = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 100)
R_Motor = GPIO.PWM(PWMB, 100)
L_Motor.start(0)
R_Motor.start(0)

bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""

def set_L_motor(speed):
    if speed > 0:
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        L_Motor.ChangeDutyCycle(speed)
    elif speed < 0:
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        L_Motor.ChangeDutyCycle(abs(speed))
    else:
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.LOW)
        L_Motor.ChangeDutyCycle(0)

def set_R_motor(speed):
    if speed > 0:
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        R_Motor.ChangeDutyCycle(speed)
    elif speed < 0:
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
        R_Motor.ChangeDutyCycle(abs(speed))
    else:
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.LOW)
        R_Motor.ChangeDutyCycle(0)

# --- 속도 100으로 수정된 함수들 ---

def go(speed=100):
    set_L_motor(speed)
    set_R_motor(-speed)
    print("ok go")

def back(speed=100):
    set_L_motor(-speed)
    set_R_motor(speed)
    print("ok back")

def left(speed=100):
    set_L_motor(-speed)
    set_R_motor(-speed)
    print("ok left")

def right(speed=100):
    set_L_motor(speed)
    set_R_motor(speed)
    print("ok right")

def stop():
    set_L_motor(0)
    set_R_motor(0)
    print("ok stop")

# --------------------------

def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()
        data = data.decode()
        gData = data

def main():
    global gData
    try:
        while True:
            if gData.find("go") >= 0:
                gData = ""
                go()
            
            elif gData.find("back") >= 0:
                gData = ""
                back()
            
            elif gData.find("left") >= 0:
                gData = ""
                left()

            elif gData.find("right") >= 0:
                gData = ""
                right()

            elif gData.find("stop") >= 0:
                gData = ""
                stop()
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    task1 = threading.Thread(target = serial_thread)
    task1.start()
    main()
    bleSerial.close()
    GPIO.cleanup()