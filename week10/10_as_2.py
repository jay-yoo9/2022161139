import cv2
import numpy as np
import os # 파일 경로 처리를 위해 추가

# 1. 실제 이미지 파일 목록 (사용자 파일 구조에 맞게 수정됨)
images = [
    '1.jpg', 
    '2.jpg', 
    '3.jpg', 
    '4.jpg'
]

# (주의: 이 스크립트(10_as_2.py)와 위 4개의 .jpg 파일이 
#  모두 'week10' 폴더 안에 있어야 합니다.)

processed_images = [] # 처리된 이미지를 저장할 리스트

for i, img_path in enumerate(images):
    print(f"처리 중: {img_path}")
    img = cv2.imread(img_path)

    if img is None:
        print(f"오류: {img_path} 파일을 로드할 수 없습니다. 파일 경로와 이름을 확인하세요.")
        continue

    # 1. 영상 크기 변경 (선택 사항, 필요에 따라 주석 해제하여 사용)
    # img = cv2.resize(img, (320, 240)) 

    # 2. 색상 공간을 HSV로 변환
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. 노란색 범위 정의 (HSV)
    # H: 색조(Hue), S: 채도(Saturation), V: 명도(Value)
    # 노란색의 대략적인 HSV 범위
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 4. 흰색 범위 정의 (HSV)
    # 흰색은 명도(V)가 높고 채도(S)가 낮은 영역
    lower_white = np.array([0, 0, 200]) # H는 무시, S 낮음, V 높음
    upper_white = np.array([180, 25, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    # (대안: BGR로 흰색 추출 - HSV 흰색 추출이 어렵다면 BGR로 시도)
    # lower_white_bgr = np.array([200, 200, 200])
    # upper_white_bgr = np.array([255, 255, 255])
    # white_mask_bgr = cv2.inRange(img, lower_white_bgr, upper_white_bgr)
    # white_mask = white_mask_bgr # 최종 흰색 마스크로 white_mask_bgr 사용

    # 5. 노란색 마스크와 흰색 마스크 합치기 (OR 연산)
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)

    # (선택) 노이즈 제거를 위한 모폴로지 연산 (opening)
    # kernel = np.ones((5,5),np.uint8)
    # combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    # combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

    # 6. 원본 이미지에 마스크 적용하여 노란색/흰색만 추출된 결과 얻기
    extracted_color_img = cv2.bitwise_and(img, img, mask=combined_mask)

    # 7. (선택) 윤곽선 검출 및 그리기
    # cv2.findContours는 흑백 이미지(combined_mask)에서 윤곽선을 찾습니다.
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 원본 이미지에 윤곽선 그리기
    contour_img = img.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 0, 255), 2)


    # 8. 결과 이미지 표시 (원본, 마스크, 추출된 색상, 윤곽선 이미지)
    # 여러 이미지를 한 창에 보여주기 위해 stack 함수 사용 (선택 사항)

    # 텍스트 오버레이 (각 이미지 위에 어떤 이미지인지 설명)
    cv2.putText(img, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(contour_img, "Contours", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(extracted_color_img, "Extracted Colors", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # 마스크 이미지는 단일 채널(흑백)이므로 3채널로 변환하여 다른 이미지와 합칠 수 있도록 합니다.
    mask_display = cv2.cvtColor(combined_mask, cv2.COLOR_GRAY2BGR)
    cv2.putText(mask_display, "Mask (Yellow + White)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)


    # --- 결과 표시 방법 (자유롭게 선택) ---

    # 방법 1: 4개 이미지를 한 창에 합쳐서 보기
    # (이미지 크기가 다를 경우 오류가 날 수 있으니, resize로 통일하는 것이 좋습니다)
    
    # 예시: 모든 이미지의 높이를 480으로 통일 (너비는 비율 유지)
    display_height = 480
    
    def resize_to_height(img_to_resize, height):
        h, w = img_to_resize.shape[:2]
        scale = height / h
        return cv2.resize(img_to_resize, (int(w * scale), height))

    try:
        img_resized = resize_to_height(img, display_height)
        mask_display_resized = resize_to_height(mask_display, display_height)
        extracted_color_img_resized = resize_to_height(extracted_color_img, display_height)
        contour_img_resized = resize_to_height(contour_img, display_height)

        top_row = cv2.hconcat([img_resized, mask_display_resized])
        bottom_row = cv2.hconcat([extracted_color_img_resized, contour_img_resized])
        
        final_display = cv2.vconcat([top_row, bottom_row])
        
        cv2.imshow(f"Image {i+1} - Line Detection", final_display)

    except Exception as e:
        print(f"이미지 스태킹 오류: {e}. 개별 창으로 표시합니다.")
        # 오류 발생 시 개별 창으로 표시 (방법 2)
        cv2.imshow(f"{img_path} - Original", img)
        cv2.imshow(f"{img_path} - Mask", combined_mask)
        cv2.imshow(f"{img_path} - Extracted", extracted_color_img)
        cv2.imshow(f"{img_path} - Contours", contour_img)

    
    # 방법 2: 4개 이미지를 개별 창으로 보기 (위 '방법 1' 부분을 주석 처리하고 이걸 사용)
    # cv2.imshow(f"{img_path} - Original", img)
    # cv2.imshow(f"{img_path} - Mask", combined_mask)
    # cv2.imshow(f"{img_path} - Extracted", extracted_color_img)
    # cv2.imshow(f"{img_path} - Contours", contour_img)
    
    # ------------------------------------

    cv2.waitKey(0) # 각 이미지마다 키 입력 대기 (다음 이미지로 넘어가기)

cv2.destroyAllWindows()