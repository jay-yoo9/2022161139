import cv2
import numpy as np

# 1. OpenCV에 내장된 Haar Cascade 얼굴 검출 분류기 로드
# 별도 XML 파일 없이 cv2.data.haarcascades 경로를 사용해 편리하게 로드할 수 있습니다.
face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# 2. 카메라 설정 (기존 코드와 동일)
cap = cv2.VideoCapture(0)  # 0번 카메라 (보통 내장 웹캠 또는 USB 카메라)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 3. 실시간 영상 처리 루프
while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("카메라를 열 수 없습니다.")
        break

    # (선택) 기존 코드처럼 카메라가 거꾸로 있다면 주석 해제
    # frame = cv2.flip(frame, 0) 

    # 화면에 표시할 원본 이미지 (scr)
    scr = frame.copy()

    # 4. 얼굴 검출을 위해 흑백(grayscale) 이미지로 변환
    # (기존 코드는 모션 감지를 위해 흑백 변환했지만, 얼굴 검출에도 흑백 이미지가 필요)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 5. 얼굴 검출 실행
    # detectMultiScale(image, scaleFactor, minNeighbors, minSize)
    # scaleFactor: 이미지 축소 비율 (너무 크면 검출 정확도 하락, 작으면 속도 저하)
    # minNeighbors: 최종 검출 영역으로 인정받기 위한 최소 이웃 사각형 개수
    # minSize: 검출할 최소 얼굴 크기
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 6. 검출된 얼굴에 사각형 표시 (과제 요구사항)
    # 'faces'는 검출된 얼굴의 [x, y, w, h] 좌표 리스트입니다.
    for (x, y, w, h) in faces:
        # (0, 255, 0): 녹색 사각형, 2: 선 두께
        cv2.rectangle(scr, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 7. 결과 영상 출력 (기존 코드와 유사)
    cv2.imshow("Face Detection", scr)

    # 8. 종료 조건 (기존 코드와 동일)
    # 'ESC' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 9. 자원 해제 (기존 코드와 동일)
cap.release()
cv2.destroyAllWindows()