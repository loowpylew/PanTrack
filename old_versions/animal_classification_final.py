# Tesseract download page: https://tesseract-ocr.github.io/tessdoc/Downloads.html 
# Direct link to both 32 and 64 bit .exe file extensions for tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# Here, we download the third party .exe file extensions for windows. By default, when installed, 
# the API's associated files can be found in program files within your PC's file system. 

# To install the tesseract python distribution, type the following in the terminal: 
# pip install pytesseract 

# To install 'opencv' which will be used to read the txt within our image/video, type the following in the terminal: 
# pip install opencv-python 

from asyncio.windows_events import NULL
from cv2 import VideoCapture
import pytesseract
import cv2
# Importing Image class from PIL module
from PIL import Image
from os import walk
import pandas as pd
import os, os.path
from pathlib import Path
import colorama 
import numpy as np 
from pynput.keyboard import  Controller
from cv2 import cvtColor

colorama.init()

def clearConsole(): 
        command = 'clear'
        if os.name in ('nt', 'dos'): 
            command = 'cls'
        os.system(command)    

class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        HACKER_GREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
config = 'digits'

temperature = []
day = []
month = []
year = []

hours = []
minutes = []
seconds = []

all_video_dirs = []

video_compatability = []

video_60s_capture = []

movement_detected_excel_input = []

cameras = NULL

movement_detected = NULL

indication_flag = NULL

#try:
print("--------------------------Excel input automation - [Animal Classification]-------------------------")
print("---------------------------------------------------------------------------------------------------")
print(f"| - {bcolors.HACKER_GREEN}In order to process all videos, you will be required to enter the directory path to which{bcolors.ENDC}     |")
print(f"|   {bcolors.HACKER_GREEN}all cameras our housed.{bcolors.ENDC}                                                                       |") 
print(f"| - {bcolors.HACKER_GREEN}The cameras have been used to record a variety of animal interactions within the habitats in{bcolors.ENDC}  |")
print(f"|   {bcolors.HACKER_GREEN}which they reside.{bcolors.ENDC}                                                                            |")
print(f"| - {bcolors.HACKER_GREEN}The number of cameras used is dependant on the professors preferenece based off their{bcolors.ENDC}         |")
print(f"|   {bcolors.HACKER_GREEN}observations on the likelihood of an animal species passing within that area of the habitat{bcolors.ENDC}   |")
print(f"|   {bcolors.HACKER_GREEN}at which observations will take place.{bcolors.ENDC}                                                        |")
print("---------------------------------------------------------------------------------------------------")    

print(f"{bcolors.HACKER_GREEN}For further details as to what this script does, please enter '{bcolors.ENDC}y{bcolors.HACKER_GREEN}', otherwise enter '{bcolors.ENDC}q{bcolors.HACKER_GREEN}' to continue: {bcolors.ENDC}")    

place_holder = True
while place_holder: 
     val = input()
     if val == 'q': 
          break 
     elif val == 'y': 
          print("""\n- Optimal Character Recognition has been used within this script to identify the watermarked dates upon creation of 
  a video as result of the camera being triggered by sudden movements.
  
- The time span of each video is around 1 - 2 minutes.

- The software has to process the file directory to where an individual video is housed, the file name of the video, 
  the watermark date/time and temperature within the video (recorded by the video camera, sensors etc), whether the 
  videos are corrupt or not and whether there is movement within the video (preferably an animal) so that the user of 
  the software is only required to watch videos with animal species in (can classify animal species) as opposed to
  watching thousands of videos where no animal activity takes place. All this information is then automatically
  loaded within an excel spreadsheet which can then be further analysed by users using a programming language such as
  a ‘R’, SPSS (data inputter) or python (same langiage used to develop this software) to perform statical models on 
  the data generated. This will save 100’s of hours of tedious identifying and inputting data as described above row
  by row, column by column within the excel spreadsheet.

- If the 60 second indicator ('60s') appears within a video, this will automatically trigger the movement detection 
  software into thinking something has moved due to the sudden differences in frames.
  For this reason, the spreadsheet will include a column to indicate whether the video contains the '60s' indicator. 
  These videos will have to be viewed manually to see if they consist of any animals for a truely accurate result. 

- The following columns will be manipulated: 

  '' - This will contain the index of each row, this is an automatic response by the ExcelWriter() function which is 
       used to write all data captured to the specified excel spreadsheet. 

  'ROW' - This column will remain empty (outside the scope of this software's purpose).

  'TREETAG' - This column will contain the camera name used to record the video within the coressponding row.

  'TREETAG_NOTES' - This column will remain empty (outside the scope of this software's purpose). 

  'FILEPATH' - This column will contain the file path of the video file. 

  'FILENAME' - This column will contain the name of the video file (excluding the file extension i.e. .AVI/.MP4).

  'YEAR' - This column will contain the year the video began recording.

  'MONTH' - This column will contain the month the video began recording.

  'DAY' - This column will contain the day the video began recording.

  'HH' - This column will contain the hour the video began recording.

  'MM' - This column will contain the minute the video began recording.

  'SS' - This column will contain the second the video began recording.

  'Common' - This column will contain either: 

           - 'None' to indicate no movement was present within the video recording. 

           - 'Corrupt' to indicate the video was not playable. 

           - '' (cell left empty) to indicate that the video has potential for animals to be present.

  'SCIENTIFIC' - This column will remain empty (outside the scope of this software's purpose).

  'QUANTITY' - This column will remain empty (outside the scope of this software's purpose).

  '60s indicator' - This column will contain either: 

                  - '60s' to indicate that the indicator appeared within the video.

                  - '' (cell left empty) to indicate that the indactor did not appear in the video.
            
   """)
         
          while True: 
               print(f"\n{bcolors.HACKER_GREEN}Please enter '{bcolors.ENDC}q{bcolors.HACKER_GREEN}' to continue to enter directory path: {bcolors.ENDC}")
               val = input()
               if val == 'q': 
                    place_holder = False
                    clearConsole()
                    break
               else: 
                    clearConsole()
                    continue
     else: 
          clearConsole()
          print(f"{bcolors.HACKER_GREEN}Please enter '{bcolors.ENDC}y{bcolors.HACKER_GREEN}', otherwise enter '{bcolors.ENDC}q{bcolors.HACKER_GREEN}' to continue: {bcolors.ENDC}")
          
print(f"\n{bcolors.HACKER_GREEN}Please enter Directory PATH: {bcolors.ENDC}", end="")
DIR = input()    

print(f"{bcolors.HACKER_GREEN}\nPlease enter the excel file name to which you wish the data to be uploaded to:{bcolors.ENDC}")

while True: 
     EXCEL_FILENAME = input()
     if len(EXCEL_FILENAME) >= 6 and ".xlsx" in EXCEL_FILENAME:
          clearConsole()
          break
     elif len(EXCEL_FILENAME) >= 6 and ".xlsx" not in EXCEL_FILENAME:
          clearConsole()
          print(f"{bcolors.HACKER_GREEN}Please enter excel filename including the '{bcolors.ENDC}.xlsx{bcolors.HACKER_GREEN}' extension: {bcolors.ENDC}")
          continue
     elif len(EXCEL_FILENAME) < 6:
          clearConsole()
          print(f"{bcolors.HACKER_GREEN}Please enter excel filename including the '{bcolors.ENDC}.xlsx{bcolors.HACKER_GREEN}' extension: {bcolors.ENDC}")
          continue 


directory_contents = os.listdir(DIR)    

print(f"\n{bcolors.HACKER_GREEN}Video cameras to be processed: {bcolors.ENDC}" + str(directory_contents) + "\n\n")    

"""for item in directory_contents:
    if os.path.isdir(item):
        cameras = item
        #print(cameras)"""
        
cameras = directory_contents
#print(cameras)

camera_count = 0     

#DIR = "D:\\CT_2020"    

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
    try:
         # Video URL
         TEST_VID = cv2.VideoCapture(directory)
         cap = cv2.VideoCapture(directory)
         READING, IMG = cap.read()    

         fourcc = cv2.VideoWriter_fourcc(*'XVID')
         out = cv2.VideoWriter('output.avi',fourcc, 5, (1280,720))
     
         ret, frame1 = cap.read()
         ret, frame2 = cap.read()  

         # Frame Number
         INDEX = 0
     
         count = 0    

         video_end_trigger = True

         keyboard = Controller()

         indication_flag = "Not Detected"

         video_60s_capture.append('No') 

         movement_detected_excel_input.append('None')

         while cap.isOpened():
             #The reason for the error is due to the video cap ending, and cv2 still trying to capture it even after the end.
             if ret == False:
                 movement_detected = "No"
                 break

             diff = cv2.absdiff(frame1, frame2) # difference between both framesq
             gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # convert to gray scale, helps discover contours 
             blur = cv2.GaussianBlur(gray, (5,5), 0) # blur gray scale frame, (5,5) - kernel size, sigma value
             _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
             dilated = cv2.dilate(thresh, None, iterations=3) # fills in holes to discover better contours 
             contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
             for contour in contours:
                 (x, y, width, height) = cv2.boundingRect(contour)    
                 if cv2.contourArea(contour) <= 500: 
                    continue

                 # roi - region of image
                 roi = frame1[y:y+height, x:x+width]

                 cv2.imwrite("images/frames/roi.jpg", roi)

                 image = cv2.imread("images/frames/roi.jpg")

                 img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)     

                 watermark_values_ROI = pytesseract.image_to_string(img_RGB, config ='--psm 4') 

                 if diff.any() == True:
                    if watermark_values_ROI[0:3] == '60S':
                        #print(watermark_values_ROI[0:3])
                        #print("Detected")
                        video_60s_capture[i] = 'Yes'
                        indication_flag = "Detected"
                    if count == 1: 
                         movement_detected = "Yes"
                         #print(i)
                         movement_detected_excel_input[i] = ""
                         #keyboard.press('q')
                         #keyboard.release('q')
                         video_end_trigger = False

                    count += 1

                 #if len(watermark_values_ROI) == 4: 
                 
                 cv2.rectangle(frame1, (x, y), (x+width, y+height), (0, 255, 0), 2)
                 cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                             1, (0, 0, 255), 3)
             #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)    

             #image = cv2.resize(frame1, (1280,720))
             #out.write(image)    

             temporary_resize = cv2.resize(frame1,(1000,500),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
             cv2.imshow("Movement Detection", temporary_resize)       

             while READING:
                 TEST_VID.set(1, INDEX)
                 READING, IMG = TEST_VID.read()
                 RET, FRAME = TEST_VID.read()       

                 NAME = "./images/frames/watermark_snippet.jpg"    

                 cv2.imwrite(NAME, FRAME)    

                 im = Image.open(NAME)    

                 # All params below are measured in pixels (px)
                 if directory.endswith('.MP4'): 
                     width, height = im.size
                     #print("Width: ", width, "Height: ", height)
                     #1920 1080
                     left = 725 # Begins at 0 for left up to maxiumum width of image 
                     top = 1050 # Begins at 0 up to maxiumum height of image
                     right = 1905 # Will exclude everything from and up to the maximum width
                     bottom = 1080 # Will exclude everything from and up to the maximum height"""    

                     imc = im.crop((left, top, right, bottom))
                     imc.save("images/frames/generated_frame.jpg")
                     #imc.show()

                     image = cv2.imread("images/frames/generated_frame.jpg")
                     img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # pytesseract API only accepts image in RGB format 
         
                     # Tesseract options for txt format styles found within images: https://muthu.co/all-tesseract-ocr-options/
                     # Known as page segmentation (option 6: Assume a single uniform block of text)    
                     watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')  

                     print(watermark_values[0:8])  # Temperature 
                     print(watermark_values[9:11])  # Day
                     print(watermark_values[12:14]) # Month     

                     print(watermark_values[15:19]) # Year
                     print(watermark_values[20:22]) # Hours 
                     print(watermark_values[23:25]) # Minutes 
                     print(watermark_values[26:28]) # Seconds"""    

                     temperature.append(watermark_values[0:8])
                     day.append(watermark_values[9:11])
                     month.append(watermark_values[12:14])
                     year.append(watermark_values[15:19])    

                     hours.append(watermark_values[20:22])
                     minutes.append(watermark_values[23:25])
                     seconds.append(watermark_values[26:28])

                     days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 
                             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
                             '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

                     months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 
                             '11', '12']
                    
                     years = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
                              '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020',
                              '2021','2022','2023','2024','2025','2026','2027','2028','2029','2030']
                              
                              
                     """,'2031','2032','2033','2034','2035','2036','2037','2038','2039','2040',
                     '2041','2042','2043','2044','2045','2046','2047','2048','2049','2050',
                     '2051','2052','2053','2054','2055','2056','2057','2058','2059','2060',
                     '2061','2062','2063','2064','2065','2066','2067','2068','2069','2070'] # 2070 is when 70% of all animal species on earth will be extinct"""
                     
                     date_in_watermark = False 
                     complete_date = month[i] + day[i] + year[i] # without semi colons to seperate day, month and year
                     day_count = 0 
                     month_count = 0 
                     year_count = 0

                     print("Complete date: ", complete_date)
                     
                     while(True):
                         possible_date = days[day_count] + months[month_count] + years[year_count]
                         #print("Possible date: ", possible_date)

                         day_count += 1
                         
                         # possible date and complete date are concentanted in reverse order given 
                         # the use of american style format of dates in watermark frames. 
                         # The arrays that hold a snippet of a possible date have been concentatnated using
                         # the english date format as written in Great Britian. 
                         if complete_date == possible_date: 
                              date_in_watermark = True 
                              break
                         else: 
                              if day_count == 31:
                                   month_count += 1
                                   if month_count == 12: 
                                        year_count += 1
                                        if year_count == 30:
                                             if day_count == 31 and month_count == 12: 
                                                  #print("Possible date: ", possible_date)
                                                  day_count = 0 
                                                  month_count = 0 
                                                  year_count = 0
                                                  break 
                                        
                                        month_count = 0       
                                   day_count = 0 

                           #issue here: index is re-initialised before being compared as the 0th index.
                         

                              
                     if date_in_watermark != True:
                         print("flag")
                         width, height = im.size
                         print("Width: ", width, "Height: ", height)
                         left = 0 # Begins at 0 for left up to maxiumum width of image 
                         top = 0 # Begins at 0 up to maxiumum height of image
                         right = 1905 # Will exclude everything from and up to the maximum width
                         bottom = 1080 # Will exclude everything from and up to the maximum height"""    

                         imc = im.crop((left, top, right, bottom))
                         imc.save("images/frames/generated_frame.jpg")
                         #imc.show()

                         image = cv2.imread("images/frames/generated_frame.jpg")
                         img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # pytesseract API only accepts image in RGB format 
         
                         # Tesseract options for txt format styles found within images: https://muthu.co/all-tesseract-ocr-options/
                         # Known as page segmentation (option 6: Assume a single uniform block of text)    
                         watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')  

                         print(watermark_values[0:8])  # Temperature 
                         print(watermark_values[9:11])  # Day
                         print(watermark_values[12:14]) # Month     

                         print(watermark_values[15:19]) # Year
                         print(watermark_values[20:22]) # Hours 
                         print(watermark_values[23:25]) # Minutes 
                         print(watermark_values[26:28]) # Seconds"""    

                         temperature.append(watermark_values[0:8])
                         day.append(watermark_values[9:11])
                         month.append(watermark_values[12:14])
                         year.append(watermark_values[15:19])    

                         hours.append(watermark_values[20:22])
                         minutes.append(watermark_values[23:25])
                         seconds.append(watermark_values[26:28])


                 elif directory.endswith('.AVI'): 
                     width, height = im.size
                     print("Width: ", width, " Height: ", height)
                     #1280 720
                     left = 800 
                     top = 690 
                     right = 1280 
                     bottom = 720 

                     imc = im.crop((left, top, right, bottom))
                     imc.save("images/frames/generated_frame.jpg")
                     #imc.show()

                     image = cv2.imread("images/frames/generated_frame.jpg")
                     img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # pytesseract API only accepts image in RGB format 
         
                     # Tesseract options for txt format styles found within images: https://muthu.co/all-tesseract-ocr-options/
                     # Known as page segmentation (option 6: Assume a single uniform block of text)    
                     watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')  

          
                     print(watermark_values[0: 2])  # Day
                     print(watermark_values[3: 5]) # Month     
                     print(watermark_values[6: 10]) # Year

                     print(watermark_values[11: 13]) # Hours 
                     print(watermark_values[14: 16]) # Minutes 
                     print(watermark_values[17: 19]) # Seconds"""  

                     day.append(watermark_values[0: 2])
                     month.append(watermark_values[3: 5])
                     year.append(watermark_values[6: 10])    

                     hours.append(watermark_values[11: 13])
                     minutes.append(watermark_values[14: 16])
                     seconds.append(watermark_values[17: 19])

                 else: 
                     print("Not an AVI/MP4 file")
                     pass    

                 #image = cv2.imread(NAME)
                 #img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                 #print(pytesseract.image_to_string(img_RGB))    

                 #cv2.imshow("Input", image)
                 #cv2.waitKey(0) # keeps input screen open
                 break # ends looping through frames     
             
             if video_end_trigger == False: 
                video_end_trigger = True
                break
          
             cv2.waitKey(1)

             frame1 = frame2
             ret, frame2 = cap.read() 

         cap.release()
         out.release()   

         
         #print(watermark_values_60s_capture[647: 652]) # captures frame with 60s indicator within video stream. output is as follows: 6 O S


         # For both .AVI and .MP4 video files, there are some where the stamp that houses the watermark 
         # along with the temperature have a larger width and height, thus the image generated as a result of
         # saving the first frame of each video will not display the section where the watermark is housed. 
         # This section is used to isolate the date and time so that we can perfrom optimal character recognition.
         # We are able to store the date and times in order to further plot within an excel spreadsheet. 
         # Thus, we have to re-specify the dimensions of the image generated that we want to isolate in order to perform
         # succesful optimal character recognition.     

         # As of time of writing, the videos supplied have 1 of 3 stamp sizings within the videos.     

         if watermark_values == '': 
              im = Image.open("images/frames/watermark_snippet.jpg")    

              width, height = im.size
              print("Width: ", width, " Height: ", height)
              # May need to be changed to accomodate both .AVI and .MP4 formats. May be anothing stamp sizing format. 
              left = 850 
              top = 675 
              right = 1250 
              bottom = 720     

              imc = im.crop((left, top, right, bottom))
              imc.save("images/frames/generated_frame.jpg")    

              image = cv2.imread("images/frames/generated_frame.jpg")
              img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)     

              watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6') 

              print(watermark_values[0: 2])  # Day
              print(watermark_values[3: 5]) # Month     
              print(watermark_values[6: 10]) # Year

              print(watermark_values[11: 13]) # Hours 
              print(watermark_values[14: 16]) # Minutes 
              print(watermark_values[17: 19]) # Seconds"""  

              day.append(watermark_values[0: 2])
              month.append(watermark_values[3: 5])
              year.append(watermark_values[6: 10])    

              hours.append(watermark_values[11: 13])
              minutes.append(watermark_values[14: 16])
              seconds.append(watermark_values[17: 19])

        
         """im = Image.open("images/frames/watermark_snippet.jpg") 
        
         width, height = im.size
         print(width, height)
         #1920 1080
         left = 600
         top = 0 
         right = 1280 
         bottom = 720            
         imc = im.crop((left, top, right, bottom))
         imc.save("images/frames/60s_indicator.jpg")          
         image = cv2.imread("images/frames/60s_indicator.jpg")
         img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # pytesseract API only accepts image in RGB format 
         
         #print(watermark_values_60s_capture[647: 652]) # captures frame with 60s indicator within video stream. output is as follows: 6 O S
         
         watermark_values_60s = pytesseract.image_to_string(img_RGB, config ='--psm 6')   
         """ 
        
         print("-----------------------------------------------------------------------------")
         print(f"{bcolors.HACKER_GREEN}Video Number: {bcolors.ENDC}" + str(i))
         print(f"{bcolors.HACKER_GREEN}Directory name: {bcolors.ENDC}" + directory)
         print(f"{bcolors.HACKER_GREEN}Watermark value: {bcolors.ENDC}" + watermark_values, end="") 
         print(f"{bcolors.HACKER_GREEN}Movement detected: {bcolors.ENDC}" + movement_detected)
         print(f"{bcolors.HACKER_GREEN}60s indicator: {bcolors.ENDC}" + indication_flag)
         print("-----------------------------------------------------------------------------")

         video_compatability.append(' ')     

    except cv2.error as e:
         video_compatability.append('Corrupt')
         print(e)
         print('Bad file:', directory) # print out the names of corrupt files   

    i += 1   



df = pd.DataFrame({'ROW': [], 'TREETAG': [], 'TREETAG_NOTES': [], 'FILEPATH': [], 
'FILENAME': [] , 'TEMPERATURE': [], 'YEAR': [], 'MONTH': [], 'DAY':[], 'HH': [], 'MM': [], 'SS':[], 'Common':[], 
'SCIENTIFIC': [], 'QUANTITY': [], '60s_INDICATOR_PRESENT': []})    
j = 0    

for file in all_video_dirs:
     try: 
          #if j < 10000:
          #print(len(all_video_dirs))
          #print(len(video_60s_capture))
          print(movement_detected_excel_input)
          file_path = str(file)
          file_name = Path(file_path).stem
          #print(file_path)
          #print(file_name)
          for camera in cameras: 
               if camera in file_path: 
                   if video_compatability[j] == "Corrupt":
                       df = df.append({'FILEPATH': file, 'FILENAME': file_name, 'Common': video_compatability[j], 'QUANTITY': 0, '60s_INDICATOR_PRESENT': video_60s_capture[j]}, ignore_index=True)      
                   elif video_compatability[j] == " " and movement_detected_excel_input == "":
                       df = df.append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'TEMPERATURE': temperature[j], 'YEAR': year[j], 'MONTH': month[j],
                                       'DAY': day[j], 'HH': hours[j], 'MM': minutes[j], 'SS': seconds[j], 'Common': movement_detected_excel_input[j], '60s_INDICATOR_PRESENT': video_60s_capture[j]}, ignore_index=True)
                   elif  video_compatability[j] == " " and movement_detected_excel_input == "None":
                       df = df.append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'TEMPERATURE': temperature[j], 'YEAR': year[j], 'MONTH': month[j],
                                       'DAY': day[j], 'HH': hours[j], 'MM': minutes[j], 'SS': seconds[j], 'Common': movement_detected_excel_input[j], 'QUANTITY': 0, '60s_INDICATOR_PRESENT': video_60s_capture[j]}, ignore_index=True)
                   
     except:
          print(f"[{bcolors.HACKER_GREEN}Exception Handled: {bcolors.ENDC}Index out of bounds{bcolors.ENDC}]")
          
     j += 1    

     #else: 
          #break
         
print(df)    

datatoexcel = pd.ExcelWriter(EXCEL_FILENAME) # engine="xlsxwriter"    

df.to_excel(datatoexcel, sheet_name='Sheet1')
datatoexcel.save()

print(f"[{bcolors.HACKER_GREEN}End of processing{bcolors.ENDC}]")
#except:
      #print(f"\n{bcolors.FAIL}KeyboardInterrupt {bcolors.ENDC}'Ctrl c' {bcolors.FAIL}has been entered")
      #print("Program adruptly ended")
              