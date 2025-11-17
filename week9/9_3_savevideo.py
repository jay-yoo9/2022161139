import numpy as np
import cv2 as cv

# 1. 입력 소스를 파일이 아닌 0번 웹캠으로 변경
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 2. 웹캠의 원본 너비와 높이를 가져옴
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# 3. 저장할 파일의 FPS를 20.0으로 고정
save_fps = 20.0

print('cap.isOpened()', cap.isOpened())
print('size', width, height)
print('fps (save)', save_fps)

# 4. 저장용 코덱 및 VideoWriter 객체 생성
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, save_fps, (width, height))

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?)")
        break

    # 5. 원본 프레임을 'output.avi' 파일에 쓰기
    out.write(frame)
    
    # 6. 화면에도 동시에 보여주기
    cv.imshow('frame', frame)

    # 7. 'q' 키를 누르면 종료
    if cv.waitKey(1) == ord('q'):
        break

# 8. 사용한 자원(카메라, 파일)을 모두 해제
cap.release()
out.release()
cv.destroyAllWindows()