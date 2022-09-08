"""
import cv2
import numpy as np

#"D:\CT_2020\\791\\05-08-20\\791-08-05082020.MP4"
#'D:\\CT_2020\\791\\05-08-20\\791-05-05082020.MP4'

animal_detected = []

cap = cv2.VideoCapture("D:\CT_2020\\791\\05-08-20\\791-08-05082020.MP4")
 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 5, (1280,720))
 
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2) # difference between both frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # convert to gray scale, helps discover contours 
    blur = cv2.GaussianBlur(gray, (5,5), 0) # blur gray scale frame, (5,5) - kernel size, sigma value
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3) # fills in holes to discover better contours 
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 3500:
            animal_detected += ""
            continue
        else: 
            animal_detected += "None"
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (1280,720))
    out.write(image)

    temporary_resize = cv2.resize(frame1,(1000,500),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    cv2.imshow("inter", temporary_resize)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()

print(animal_detected)

"""
 
import cv2
from cv2 import cvtColor
from cv2 import Canny
import numpy as np
import os, os.path
import numpy as np 
from pynput.keyboard import Key, Controller

#"D:\CT_2020\\791\\05-08-20\\791-08-05082020.MP4"
#'D:\\CT_2020\\791\\05-08-20\\791-05-05082020.MP4'

#"D:\\CT_2020\\4820\\26-03-20\\4820-55-26032020.AVI"

all_video_dirs = []

video_compatability = []

animal_detected = []



DIR ='D:\\CT_2020'

for root, dirs, files in os.walk(DIR): 
    for file in files:
        if file.endswith('.AVI') or file.endswith('.MP4'): 
            all_video_dirs.append(os.path.join(root, file))

#print(all_video_dirs)    

i = 0    

for files in all_video_dirs: 

    #if i == 10000:
        #break
    directory = str(files)
    #print(directory)
    

    cap = cv2.VideoCapture(directory)
     
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 5, (1280,720))
     
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()  

    count = 0
    val = ''
    keyboard = Controller()

    while cap.isOpened():
        #The reason for the error is due to the video cap ending, and cv2 still trying to capture it even after the end.
        if ret == False:
            print("No movement")
            animal_detected = "None"
            break

        diff = cv2.absdiff(frame1, frame2) # difference between both framesq
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # convert to gray scale, helps discover contours 
        blur = cv2.GaussianBlur(gray, (5,5), 0) # blur gray scale frame, (5,5) - kernel size, sigma value
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3) # fills in holes to discover better contours 
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)    
            if cv2.contourArea(contour) < 1000: 
                continue

            if diff.any() == True: 
                if count == 1: 
                    print("Movement detected")
                    animal_detected = ""
                    #keyboard.press('q')
                    #keyboard.release('q')
                    val = 'end'
                count += 1

            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
        #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)    

        #image = cv2.resize(frame1, (1280,720))
        #out.write(image)    

        temporary_resize = cv2.resize(frame1,(1000,500),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        cv2.imshow("inter", temporary_resize)    

        frame1 = frame2
        ret, frame2 = cap.read()    
        
        if val == 'end': 
            val = ''
            break
        
        cv2.waitKey(1)
        
        """if cv2.waitKey(1) == ord('q'):
            count = 0
            break"""
            
        """if cv2.waitKey(1) == 27: 
            break"""

    #cv2.destroyAllWindows()
    cap.release()
    out.release()    


 
