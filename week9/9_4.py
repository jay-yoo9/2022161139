import numpy as np
import cv2 as cv

# 1. 마우스 이벤트가 발생할 때마다 호출될 함수(콜백 함수)를 정의합니다.
def draw_circle(event, x, y, flags, param):
    
    # 만약 이벤트가 "왼쪽 버튼 더블 클릭"이면
    if event == cv.EVENT_LBUTTONDBLCLK:
        # (x,y) 좌표에 반지름 10, 파란색(255,0,0)으로 채워진(-1) 원을 그립니다.
        cv.circle(img, (x, y), 10, (255, 0, 0), -1)

# 2. 원을 그릴 검은색 바탕 이미지(512x512)를 만듭니다.
img = np.zeros((512, 512, 3), np.uint8)

# 3. 'image'라는 이름의 새 창을 만듭니다.
cv.namedWindow('image')

# 4. (가장 중요) 'image' 창에서 마우스 이벤트가 발생하면, 'draw_circle' 함수를 실행하도록 연결합니다.
cv.setMouseCallback('image', draw_circle)

while(1):
    # 5. 'img' 이미지를 'image' 창에 계속해서 보여줍니다.
    cv.imshow('image', img)
    
    # 6. ESC 키를 누르면 프로그램이 종료됩니다.
    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()