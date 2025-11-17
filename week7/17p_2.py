import RPi.GPIO as GPIO
import time

PWMA = 18
AIN1 = 22
AIN2 = 27
PWMB = 23
BIN1 = 24
BIN2 = 25

sw_pins = [5, 6, 13, 19]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

for pin in sw_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

L_Motor = GPIO.PWM(PWMA, 500)
L_Motor.start(0)
R_Motor = GPIO.PWM(PWMB, 500)
R_Motor.start(0)

def go_forward(speed):
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    R_Motor.ChangeDutyCycle(speed)

def go_backward(speed):
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    R_Motor.ChangeDutyCycle(speed)

def turn_left(speed):
    GPIO.output(AIN1, 1)
    GPIO.output(AIN2, 0)
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, 1)
    GPIO.output(BIN2, 0)
    R_Motor.ChangeDutyCycle(speed)

def turn_right(speed):
    GPIO.output(AIN1, 0)
    GPIO.output(AIN2, 1)
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN1, 0)
    GPIO.output(BIN2, 1)
    R_Motor.ChangeDutyCycle(speed)

def stop():
    L_Motor.ChangeDutyCycle(0)
    R_Motor.ChangeDutyCycle(0)

print("스위치로 자동차를 조종하세요. (종료: Ctrl+C)")

try:
    while True:
        sw1_state = GPIO.input(sw_pins[0])
        sw2_state = GPIO.input(sw_pins[1])
        sw3_state = GPIO.input(sw_pins[2])
        sw4_state = GPIO.input(sw_pins[3])

        if sw1_state == 1:
            print("SW1: 앞")
            go_forward(70)
        elif sw2_state == 1:
            print("SW2: 오른쪽")
            turn_right(70)
        elif sw3_state == 1:
            print("SW3: 왼쪽")
            turn_left(70)
        elif sw4_state == 1:
            print("SW4: 뒤")
            go_backward(70)
        else:
            stop()
        
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
    pass

finally:
    GPIO.cleanup()