import RPi.GPIO as GPIO
import time

BUZZER_PIN = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 1.0)
pwm.start(0) 

scale = {
    'Do': 262, 'Re': 294, 'Mi': 330, 'Fa': 349, 
    'Sol': 392, 'La': 440, 'Si': 494, 'high_Do': 523
}

try:
    for note_hz in scale.values():
        print(f"연주 중인 음계 주파수: {note_hz}Hz")
        pwm.ChangeFrequency(note_hz) 
        pwm.ChangeDutyCycle(50) 
        time.sleep(0.5) 
        pwm.ChangeDutyCycle(0) 
        time.sleep(0.1) 

except KeyboardInterrupt:
    print("\n연주를 중단합니다.")

finally:
    pwm.stop()
    GPIO.cleanup()