# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 1. 사용할 GPIO 핀 설정 (BCM 모드 기준)
# (pinout에서 확인한 5, 6, 13, 19번 핀)
sw_pins = [5, 6, 13, 19] 

# 2. 과제 요구사항을 위한 리스트 (4번 요구사항: 리스트 활용)
# 스위치 이름 리스트 (2번 요구사항: "click x" 형태)
sw_names = ['SW1 click', 'SW2 click', 'SW3 click', 'SW4 click']
# 스위치의 이전 상태 저장을 위한 리스트 (4번 요구사항)
prev_states = [0, 0, 0, 0]
# 스위치별 클릭 횟수 저장을 위한 리스트 (4번 요구사항: 누적 횟수)
click_counts = [0, 0, 0, 0]

# GPIO 설정
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) # BCM 모드 사용

# sw_pins 리스트의 모든 핀을 입력(IN) 모드로 설정
for pin in sw_pins:
    # 내부 풀다운 저항(PUD_DOWN) 사용
    # : 스위치를 안 누르면 0V(0), 누르면 3.3V(1)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # 4개의 스위치를 반복문으로 순회
        for i in range(len(sw_pins)):
            # 현재 핀(sw_pins[i])의 상태 읽기 (0 또는 1)
            current_state = GPIO.input(sw_pins[i])
            
            # 3. 스위치가 눌리는 순간(0 -> 1) 감지 (1번, 3번 요구사항)
            # (이전 상태는 0 이었고, 현재 상태는 1 인지 확인)
            if current_state == 1 and prev_states[i] == 0:
                
                # 해당 스위치의 클릭 횟수 1 증가
                click_counts[i] += 1 
                
                # 4. 과제에서 요구한 출력 형식
                # 예: ('SW1 click', 1)
                print(f"('{sw_names[i]}', {click_counts[i]})")

            # 4. 다음 루프를 위해 현재 상태를 '이전 상태' 리스트에 저장
            prev_states[i] = current_state
            
        # 너무 빠른 반복을 방지하여 CPU 부담을 줄이고,
        # 스위치의 물리적인 떨림(Chattering)을 방지
        time.sleep(0.05) 

except KeyboardInterrupt:
    # Ctrl+C 입력 시
    print("\n프로그램을 종료합니다.")
    pass

finally:
    # 프로그램 종료 시 GPIO 핀 설정 초기화
    GPIO.cleanup()