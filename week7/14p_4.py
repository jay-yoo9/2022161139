import RPi.GPIO as GPIO
import time

sw_pins = [5, 6, 13, 19]
BUZZER_PIN = 12

notes = ['Mi', 'Fa', 'Sol', 'La']
scale = {
    'Mi': 330,
    'Fa': 349, 
    'Sol': 392, 
    'La': 440
}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in sw_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 1.0)
pwm.start(0) 

current_note_hz = 0

print("4키 피아노를 연주하세요. (종료: Ctrl+C)")
print(f"SW1:{notes[0]}, SW2:{notes[1]}, SW3:{notes[2]}, SW4:{notes[3]}")

try:
    while True:
        key_pressed = False
        
        for i in reversed(range(len(sw_pins))):
            if GPIO.input(sw_pins[i]) == 1:
                key_pressed = True
                note_name = notes[i]
                note_hz = scale[note_name]
                
                if current_note_hz != note_hz:
                    pwm.ChangeFrequency(note_hz)
                    pwm.ChangeDutyCycle(50)
                    current_note_hz = note_hz
                    print(f"Play: {note_name} ({note_hz}Hz)")
                
                break
        
        if not key_pressed:
            if current_note_hz != 0:
                pwm.ChangeDutyCycle(0)
                current_note_hz = 0
                print("Stop")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n연주를 종료합니다.")

finally:
    pwm.stop()
    GPIO.cleanup()