import cv2 as cv
import numpy as np
import threading, time
import SDcar
import sys

DRIVE_SPEED = 50
EPSILON = 1e-6
ROI_Y_START = 170
LINE_TOLERANCE = 0.15
TURN_OFFSET = 60

v_x = 320
v_y = 240
img_center_x = v_x // 2
g_moment_history = np.array([0, 0, 0])
g_thread_running = True
g_auto_drive_enabled = False
g_car = None

def keep_alive_thread():
    i = 0
    while True:
        time.sleep(1)
        i = i+1
        if g_thread_running is False:
            break

def handle_keyboard_input(which_key):
    is_exit = False
    global g_auto_drive_enabled
    
    if which_key & 0xFF == 184:
        print('up')
        g_car.motor_go(DRIVE_SPEED)
    elif which_key & 0xFF == 178:
        print('down')
        g_car.motor_back(DRIVE_SPEED)
    elif which_key & 0xFF == 180:
        print('left')
        g_car.motor_left(DRIVE_SPEED)
    elif which_key & 0xFF == 182:
        print('right')
        g_car.motor_right(DRIVE_SPEED)
    elif which_key & 0xFF == 181:
        g_car.motor_stop()
        print('stop')
    elif which_key & 0xFF == ord('q'):
        g_car.motor_stop()
        print('exit')
        is_exit = True
    elif which_key & 0xFF == ord('e'):
        g_auto_drive_enabled = True
        print('enable_linetracing:', g_auto_drive_enabled)
        g_car.motor_go(DRIVE_SPEED)
    elif which_key & 0xFF == ord('w'):
        g_auto_drive_enabled = False
        g_car.motor_stop()
        print('enable_linetracing 2:', g_auto_drive_enabled)
    return is_exit

def detect_maskY_HSV(frame):
    crop_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    crop_hsv = cv.GaussianBlur(crop_hsv, (5,5), cv.BORDER_DEFAULT)
    mask_Y = cv.inRange(crop_hsv, (20, 50, 50), (40, 255, 255))
    return mask_Y

def detect_maskY_BGR(frame):
    B = frame[:,:,0]
    G = frame[:,:,1]
    R = frame[:,:,2]
    Y = np.zeros_like(G, np.uint8)
    Y = G*0.5 + R*0.5 - B*0.7
    Y = Y.astype(np.uint8)
    Y = cv.GaussianBlur(Y, (5,5), cv.BORDER_DEFAULT)
    _, mask_Y = cv.threshold(Y, 100, 255, cv.THRESH_BINARY)
    return mask_Y

def perform_line_tracing(cx):
    global g_moment_history
    global v_x
    
    diff = 0
    
    if g_moment_history[0] != 0 and g_moment_history[1] != 0 and g_moment_history[2] != 0:
        avg_m = np.mean(g_moment_history)
        diff = np.abs(avg_m - cx) / v_x
    
    if diff <= LINE_TOLERANCE:
        g_moment_history[0] = g_moment_history[1]
        g_moment_history[1] = g_moment_history[2]
        g_moment_history[2] = cx
        
        if cx < (img_center_x - TURN_OFFSET): 
            g_car.motor_left(DRIVE_SPEED)
            print('turn left')
        
        elif cx > (img_center_x + TURN_OFFSET): 
            g_car.motor_right(DRIVE_SPEED)
            print('turn right')
            
        else: 
            g_car.motor_go(DRIVE_SPEED)
            print('go')
            
    else:
        g_car.motor_stop() 
        print('Lost line or Sudden change! STOP!')
        g_moment_history = [0,0,0]

def draw_helper_lines(img):
    h, _, _ = img.shape
    left_line_x = img_center_x - TURN_OFFSET
    right_line_x = img_center_x + TURN_OFFSET
    
    cv.line(img, (left_line_x, 0), (left_line_x, h), (0, 255, 0), 1)
    cv.line(img, (right_line_x, 0), (right_line_x, h), (0, 255, 0), 1)

def main():
    global g_thread_running 
    
    camera = cv.VideoCapture(0)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, v_x) 
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, v_y)
    
    try:
        while( camera.isOpened() ):
            ret, frame = camera.read()
            frame = cv.flip(frame,-1)
            cv.imshow('Full Camera View', frame) 
            
            crop_img = frame[ROI_Y_START:,:]
            maskY = detect_maskY_HSV(crop_img)
            
            contours, _ = cv.findContours(maskY, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                c = max(contours, key=cv.contourArea)
                m = cv.moments(c)
                
                if m['m00'] > EPSILON:
                    cx = int(m['m10'] / m['m00'])
                    cy = int(m['m01'] / m['m00'])
                else:
                    cx = img_center_x
                    cy = 0
                
                cv.circle(crop_img, (cx,cy), 3, (0,0,255),-1)
                cv.drawContours(crop_img, contours, -1, (0,255,0), 3) 
                cv.putText(crop_img, str(cx), (10, 10), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0))
                
                if g_auto_drive_enabled == True:
                    perform_line_tracing(cx)
            
            elif g_auto_drive_enabled == True:
                print("No line detected. STOP!")
                g_car.motor_stop()
                g_moment_history = [0,0,0] 
                
            draw_helper_lines(crop_img)
            cv.imshow('crop_img', cv.resize(crop_img, dsize=(0,0), fx=2, fy=2))
            
            is_exit = False
            which_key = cv.waitKey(20)
            
            if which_key > 0:
                is_exit = handle_keyboard_input(which_key)
            if is_exit is True:
                cv.destroyAllWindows()
                break
                
    except Exception as e:
        print(e)
        g_thread_running = False

if __name__ == '__main__':
    g_moment_history = np.array([0, 0, 0])
    
    t_task1 = threading.Thread(target = keep_alive_thread)
    t_task1.start()
    
    g_car = SDcar.Drive()
    
    g_thread_running = True
    g_auto_drive_enabled = False
    
    main() 
    
    g_thread_running = False
    g_car.clean_GPIO()
    print('end vis')