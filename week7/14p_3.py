import RPi.GPIO as GPIO
import time

sw_pins = [5, 6, 13, 19] 
BUZZER_PIN = 12

HORN_FREQ = 440
HORN_DURATION = 0.3 

prev_states = [0, 0, 0, 0]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in sw_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 1.0) 
pwm.start(0) 

print("스위치를 눌러 경적을 울리세요. (종료: Ctrl+C)")

try:
    while True:
        for i in range(len(sw_pins)):
            current_state = GPIO.input(sw_pins[i])
            
            if current_state == 1 and prev_states[i] == 0:
                
                print(f"SW{i+1} 눌림! 경적!")
                
                pwm.ChangeFrequency(HORN_FREQ)
                pwm.ChangeDutyCycle(50)
                time.sleep(HORN_DURATION)
                pwm.ChangeDutyCycle(0)

            prev_states[i] = current_state
            
        time.sleep(0.05) 

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
    pass

finally:
    pwm.stop()
    GPIO.cleanup()