import cv2  
import imutils
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

file_path = 0

def set_file_path():
    global file_path
    file_path = filedialog.askopenfilename(title="Select Video", filetypes=[("Video files", "*.mp4;")])
    vidcap = cv2.VideoCapture(file_path)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    frameCount = 0
    timestart = 0
    speed = 0
    xstart = 0

    while vidcap.isOpened():
        ret, frame = vidcap.read()

        frame = imutils.resize(frame, 1080)
        
        #check whether frame is successfully captured
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = fgbg.apply(frame)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_contour_area = 1200

            # Check if motion is detected
            motion_detected = any(cv2.contourArea(contour) > min_contour_area for contour in contours)
            if motion_detected:
                largest = sorted(contours, key=cv2.contourArea, reverse=True)[0]
                area = cv2.contourArea(largest)
                
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    
                    if frameCount == 0:
                        timestart = time.time()
                        xstart, ystart = cx, cy
                        
                    if frameCount == 39:
                        t = time.time() - timestart
                        d = ((cx - xstart)**2 + (cy - ystart)**2)**0.5
                        d = d / 6.646
                        speed = d / t 
                        speed = speed / 3.6
                        speed = round(speed, 3)

                    frameCount = (frameCount + 1) % 40
                    cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
                    cv2.putText(frame, "Speed " + str(speed) + " km/h", (cx-20, cy-20), None, 2, (10, 20, 250), 3)

            cv2.imshow("Frame",frame)
    
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break

        else:
            print("Error : Failed to capture frame")

    else:
        print("Cannot open camera")
        

def real_time():
    global file_path
    file_path = 0
    vidcap = cv2.VideoCapture(file_path)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    frameCount = 0
    timestart = 0
    speed = 0
    xstart = 0

    while vidcap.isOpened():
        ret, frame = vidcap.read()

        frame = imutils.resize(frame, 1080)

        #check whether frame is successfully captured
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = fgbg.apply(frame)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_contour_area = 1200

            # Check if motion is detected
            motion_detected = any(cv2.contourArea(contour) > min_contour_area for contour in contours)
            if motion_detected:
                largest = sorted(contours, key=cv2.contourArea, reverse=True)[0]
                area = cv2.contourArea(largest)
                
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])
                    
                    if frameCount == 0:
                        timestart = time.time() * 1000
                        xstart, ystart = cx, cy
                        
                    if frameCount == 59:
                        t = (time.time() * 1000) - timestart
                        d = ((cx - xstart)**2 + (cy - ystart)**2)**0.5
                        d = d / 6.646
                        speed = d / (t/1000.0) 
                        speed = speed / 3.6
                        speed = round(speed, 3)

                    cv2.putText(frame, "Speed " + str(speed) + " km/h", (cx-20, cy-20), None, 2, (10, 20, 250), 3)
                    frameCount = (frameCount + 1) % 60
                    cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)

            cv2.imshow("Frame",frame)
   
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break

        else:
            print("Error : Failed to capture frame")

    else:
        print("Cannot open camera")
        

root = tk.Tk()

frame= ttk.Frame(root)

button= ttk.Button(frame, text= "Choose Video", command= set_file_path)
button.pack(padx = 10, pady = 10, side = tk.LEFT)
button= ttk.Button(frame, text= "Real Time", command= real_time)
button.pack(padx = 10, pady = 10, side = tk.LEFT)
frame.pack(padx = 20, pady = 20)
root.mainloop()