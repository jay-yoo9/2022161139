import threading
import time
import RPi.GPIO as GPIO

class Drive:
    def __init__(self):
        # 핀 번호를 BCM 모드 기준으로 설정
        self.pins = {"SW1": 5, "SW2": 6, "SW3": 13, "SW4": 19,
                     "PWMA": 18, "AIN1": 22, "AIN2": 27,
                     "PWMB": 23, "BIN1": 25, "BIN2": 24}
        self.config_GPIO()
        # 좌우 모터 PWM 설정
        self.L_Motor = GPIO.PWM(self.pins["PWMA"], 500)
        self.L_Motor.start(0)
        self.R_Motor = GPIO.PWM(self.pins["PWMB"], 500)
        self.R_Motor.start(0)

    def config_GPIO(self):
        # GPIO 핀 설정
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins["SW1"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["SW2"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["SW3"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["SW4"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pins["PWMA"], GPIO.OUT)
        GPIO.setup(self.pins["AIN1"], GPIO.OUT)
        GPIO.setup(self.pins["AIN2"], GPIO.OUT)
        GPIO.setup(self.pins["PWMB"], GPIO.OUT)
        GPIO.setup(self.pins["BIN1"], GPIO.OUT)
        GPIO.setup(self.pins["BIN2"], GPIO.OUT)

    def clean_GPIO(self):
        # GPIO 설정 초기화
        GPIO.cleanup()

    def motor_go(self, speed):
        # 전진
        GPIO.output(self.pins["AIN1"], 0)
        GPIO.output(self.pins["AIN2"], 1)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.pins["BIN1"], 0)
        GPIO.output(self.pins["BIN2"], 1)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_back(self, speed):
        # 후진
        GPIO.output(self.pins["AIN1"], 1)
        GPIO.output(self.pins["AIN2"], 0)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.pins["BIN1"], 1)
        GPIO.output(self.pins["BIN2"], 0)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_left(self, speed):
        # 좌회전 (왼쪽 바퀴 후진, 오른쪽 바퀴 전진)
        GPIO.output(self.pins["AIN1"], 1)
        GPIO.output(self.pins["AIN2"], 0)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.pins["BIN1"], 0)
        GPIO.output(self.pins["BIN2"], 1)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_right(self, speed):
        # 우회전 (왼쪽 바퀴 전진, 오른쪽 바퀴 후진)
        GPIO.output(self.pins["AIN1"], 0)
        GPIO.output(self.pins["AIN2"], 1)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.pins["BIN1"], 1)
        GPIO.output(self.pins["BIN2"], 0)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_stop(self):
        # 정지
        GPIO.output(self.pins["AIN1"], 0)
        GPIO.output(self.pins["AIN2"], 1)
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.pins["BIN1"], 0)
        GPIO.output(self.pins["BIN2"], 1)
        self.R_Motor.ChangeDutyCycle(0)

if __name__ == '__main__':
    # 이 파일(SDCar.py)을 직접 실행할 때 모터 테스트
    drive = Drive()
    print("Testing motor_go...")
    drive.motor_go(100)
    time.sleep(2)
    print("Testing motor_left...")
    drive.motor_left(100)
    time.sleep(2)
    print("Testing motor_right...")
    drive.motor_right(100)
    time.sleep(2)
    print("Testing motor_back...")
    drive.motor_back(100)
    time.sleep(2)
    print("Test complete. Cleaning up GPIO...")
    drive.clean_GPIO()