import cv2 as cv
import numpy as np
import threading, time
import SDcar  # 1번에서 만든 SDCar.py 모듈을 임포트
import sys

# --- 전역 변수 설정 ---
speed = 30       # 주행 속도
epsilon = 0.0001 # 0으로 나누기 방지

# --- 헬퍼 함수 정의 ---

def detect_maskY_HSV(frame):
    """
    HSV 색 공간을 사용해 노란색 영역을 검출합니다. (15p)
    """
    crop_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    crop_hsv = cv.GaussianBlur(crop_hsv, (5,5), cv.BORDER_DEFAULT)
    
    # H(색상), S(채도), V(명도) 값으로 노란색 범위 설정 (환경에 맞게 튜닝 필요)
    mask_Y = cv.inRange(crop_hsv, (25, 50, 100), (35, 255, 255))
    return mask_Y

def show_grid(img):
    """
    이미지(crop_img)에 10등분된 세로 그리드 선을 그립니다. (22p)
    """
    h, w = img.shape[:2]
    for x in v_x_grid:
        cv.line(img, (x, 0), (x, h), (0,255,0), 1, cv.LINE_4)

def line_tracing(cx):
    """
    검출된 라인의 x좌표(cx)를 바탕으로 모터를 제어합니다. (23p)
    """
    global moment, v_x
    tolerance = 0.1 # 중심점 떨림 허용치 (10%)
    diff = 0
    
    # 1. 모멘트 버퍼(최근 3개 cx)가 채워졌는지 확인
    if moment[0] != 0 and moment[1] != 0 and moment[2] != 0:
        avg_m = np.mean(moment) # 평균 계산
        diff = np.abs(avg_m - cx) / v_x # 현재 cx와 평균의 차이(비율)
        print('diff   :.4f '.format(diff))
        
        # 2. 차이가 허용치(tolerance) 이내일 때만 조향 (떨림 방지)
        if diff <= tolerance:
            # 2-1. 모멘트 버퍼 업데이트 (가장 오래된 값 빼고 새 값 추가)
            moment[0] = moment[1]
            moment[1] = moment[2]
            moment[2] = cx
            
            # 2-2. 조향 로직 (그리드 기준)
            if v_x_grid[2] <= cx < v_x_grid[3]:
                car.motor_go(speed)
                print('go')
            elif v_x_grid[3] <= cx: # 중심이 오른쪽에 치우침 -> 좌회전
                car.motor_left(speed)
                print('turn left')
            elif v_x_grid[1] >= cx: # 중심이 왼쪽에 치우침 -> 우회전
                car.motor_right(speed)
                print('turn right')
        
        # 3. 차이가 허용치를 넘으면(노이즈), 일단 직진하고 버퍼 초기화
        else:
            car.motor_go(speed)
            print('go (diff too high)')
            moment = np.array([0,0,0])
            
    # 4. 모멘트 버퍼가 비어있으면(초기 3 프레임) 채웁니다.
    elif moment[0] == 0:
        moment[0] = cx
    elif moment[1] == 0:
        moment[1] = cx
    elif moment[2] == 0:
        moment[2] = cx
        print("Moment buffer initialized.")


def func_thread():
    """
    메인 스레드와 별도로 "alive!!"를 1초마다 출력하는 스레드 함수 (9p)
    """
    i = 0
    while True:
        print("alive!!")
        time.sleep(1)
        i = i+1
        if is_running is False: # 메인 스레드 종료 시 함께 종료
            break

def key_cmd(which_key):
    """
    키 입력을 받아 모터를 제어하거나 자율주행을 토글합니다. (21p 수정본)
    """
    print('which_key', which_key)
    is_exit = False
    global enable_linetracing # 'e', 'w' 키로 값을 변경하므로 global 선언

    if which_key & 0xFF == 184: # 숫자패드 8
        print('up')
        car.motor_go(speed)
    elif which_key & 0xFF == 178: # 숫자패드 2
        print('down')
        car.motor_back(speed)
    elif which_key & 0xFF == 180: # 숫자패드 4
        print('left')
        car.motor_left(speed)
    elif which_key & 0xFF == 182: # 숫자패드 6
        print('right')
        car.motor_right(speed)
    elif which_key & 0xFF == 181: # 숫자패드 5
        car.motor_stop()
        print('stop')
    elif which_key & 0xFF == ord('q'):
        car.motor_stop()
        print('exit')
        is_exit = True
        
    # 'e' 키: 자율주행 시작
    elif which_key & 0xFF == ord('e'):
        enable_linetracing = True
        print('enable_linetracing:', enable_linetracing)
    # 'w' 키: 자율주행 중지
    elif which_key & 0xFF == ord('w'):
        enable_linetracing = False
        car.motor_stop() # 자율주행 종료 시 정지
        print('enable_linetracing 2:', enable_linetracing)
        
    return is_exit 

def main():
    """
    메인 함수: 카메라 캡처, 영상 처리, 키 입력 처리를 반복 (10p)
    """
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, v_x)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, v_y)
    
    try:
        while( camera.isOpened() ):
            ret, frame = camera.read()
            frame = cv.flip(frame, -1)

            # --- 영상 처리 시작 (12p ~ 20p) ---
            
            # 1. 영상 자르기 (ROI)
            # (120 -> 180으로 변경됨, 환경에 맞게 조절)
            crop_img = frame[180:,:] 
            
            # 2. 노란색 라인 검출
            maskY = detect_maskY_HSV(crop_img) 
            
            # 3. 컨투어(외곽선) 찾기
            contours, _ = cv.findContours(maskY, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
            # 4. 컨투어가 있으면 모멘트 계산
            if len(contours) > 0:
                c = max(contours, key=cv.contourArea) # 가장 큰 컨투어 선택
                m = cv.moments(c) # 모멘트 계산
                
                # 5. 무게 중심(Centroid) x, y 좌표 계산
                cx = int(m['m10']/(m['m00']+epsilon))
                cy = int(m['m01']/(m['m00']+epsilon))
                
                # 6. 찾은 중심과 컨투어 시각화
                cv.circle(crop_img, (cx,cy), 3, (0,0,255), -1)
                cv.drawContours(crop_img, [c], -1, (0,255,0), 3)
                
                # 7. cx 좌표값 화면에 표시
                cv.putText(crop_img, str(cx), (10, 10), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0))
                
                # 8. 자율주행 모드('e'키)가 켜졌다면 조향 함수 호출
                if enable_linetracing == True:
                    line_tracing(cx)
            
            # 9. 그리드 표시
            show_grid(crop_img)
            
            # 10. 최종 처리 영상(2배 확대) 출력
            cv.imshow('crop_img', cv.resize(crop_img, dsize=(0,0), fx=2, fy=2))
            
            # --- 영상 처리 종료 ---

            is_exit = False
            which_key = cv.waitKey(20) # 20ms 키 입력 대기
            if which_key > 0:
                is_exit = key_cmd(which_key)
            if is_exit is True:
                cv.destroyAllWindows()
                break
                
    except Exception as e:
        print(e)
        global is_running
        is_running = False # 예외 발생 시 스레드 종료

# --- 메인 코드 실행 (8p, 22p) ---
if __name__ == '__main__':

    v_x = 320 # 카메라 가로 해상도
    v_y = 240 # 카메라 세로 해상도

    # --- 전역 변수 초기화 ---
    v_x_grid = [int(v_x*i/10) for i in range(1, 10)] # 그리드 좌표
    moment = np.array([0, 0, 0]) # 모멘트 버퍼
    print(v_x_grid)
    
    t_task1 = threading.Thread(target = func_thread)
    t_task1.start()

    car = SDcar.Drive()
    
    is_running = True
    enable_linetracing = False # 자율주행 모드 플래그 (초기값: False)
    
    main() # 메인 함수 실행
    
    is_running = False # 스레드 종료 신호
    car.clean_GPIO()
    print('end vis')