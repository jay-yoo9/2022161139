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

melody = [
    ('Sol', 0.2), ('Sol', 0.2), ('Fa', 0.3),
    ('Rest', 0.1), 
    ('Fa', 0.2), ('Fa', 0.2), ('Mi', 0.3),
    ('Rest', 0.1), 
    ('Mi', 0.25),
    ('Rest', 0.05), 
    ('Sol', 0.2), ('Fa', 0.2), ('Mi', 0.4)
]

try:
    print("쿨(Cool) - '애상' (도입부) 연주를 다시 시작합니다! 🎶")
    
    for note_name, duration in melody:
        
        if note_name == 'Rest':
            print(" (쉼표) ")
            pwm.ChangeDutyCycle(0) 
        else:
            note_hz = scale[note_name]
            
            print(f"연주 중: {note_name} ({note_hz}Hz), {duration}초")
            
            pwm.ChangeFrequency(note_hz)  
            pwm.ChangeDutyCycle(50)       
        
        time.sleep(duration)
        
        pwm.ChangeDutyCycle(0)
        time.sleep(0.05) 

except KeyboardInterrupt:
    print("\n연주를 중단합니다.")

finally:
    pwm.stop()
    GPIO.cleanup()