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

day = []
month = []
year = []

hours = []
minutes = []
seconds = []

all_video_dirs = []

video_compatability = []

cameras = NULL

#try:
print("----------------------------Excel input automation watermark script--------------------------------")
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
          print("""\n- Optimal Character Recognition has been used within this script to identify the watermarked dates upon creation of a video as result of the camera being triggered by sudden movements.
                     - The time span of each video is around 1 - 2 minutes.
                     - The software has to process the file directory to where an individual video is housed, the file name of the video, the watermark date/time and temperature within the video (recorded by 
                       the video camera, sensors etc), whether the videos are corrupt or not and whether there is movement within the video (preferably an animal) so that the user of the software is only required 
                       to watch videos with animal species in (can classify animal species) as opposed to watching thousands of videos where no animal activity takes place. All this information is then automatically
                       loaded within an excel spreadsheet which can then be further analysed by lectures using a programming language known a ‘R’ to perform statical models on the data generated. This will save 100’s 
                       of hours of tedious identifying and inputting all data as describes above row by row, column by column within the excel spreadsheet.""")
         
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
        #     
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
         READING, IMG = TEST_VID.read()    

         # Frame Number
         INDEX = 0
     
         count = 0    

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
                 #print(width, height)
                 #1920 1080
                 left = 1540 # Begins at 0 for left up to maxiumum width of image 
                 top = 1050 # Begins at 0 up to maxiumum height of image
                 right = 1905 # Will exclude everything from and up to the maximum width
                 bottom = 1080 # Will exclude everything from and up to the maximum height"""    

                 imc = im.crop((left, top, right, bottom))
                 imc.save("images/frames/generated_frame.jpg")
                 #imc.show()
             elif directory.endswith('.AVI'): 
                 #width, height = im.size
                 #print(width, height)
                 #1280 720
                 left = 800 
                 top = 690 
                 right = 1280 
                 bottom = 720 

                 imc = im.crop((left, top, right, bottom))
                 imc.save("images/frames/generated_frame.jpg")
                 #imc.show()
             else: 
                 print("Not an AVI/MP4 file")
                 pass    

             #image = cv2.imread(NAME)
             #img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
             #print(pytesseract.image_to_string(img_RGB))    

             #cv2.imshow("Input", image)
             #cv2.waitKey(0) # keeps input screen open
             break # ends looping through frames     

         image = cv2.imread("images/frames/generated_frame.jpg")
         img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # pytesseract API only accepts image in RGB format 
         # Tesseract options for txt format styles found within images: https://muthu.co/all-tesseract-ocr-options/
         # Known as page segmentation (option 6: Assume a single uniform block of text)    

         watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')    

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
              #print(width, height)
              # My need to be changed to accomodate both .AVI and .MP4 formats. May be anothing stamp sizing format. 
              left = 850 
              top = 675 
              right = 1250 
              bottom = 720     

              imc = im.crop((left, top, right, bottom))
              imc.save("images/frames/generated_frame.jpg")    

              image = cv2.imread("images/frames/generated_frame.jpg")
              img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)     

              watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')    


         print(f"{bcolors.HACKER_GREEN}Video Number: {bcolors.ENDC}" + str(i))
         print(f"{bcolors.HACKER_GREEN}Directory name: {bcolors.ENDC}" + directory)
         print(f"{bcolors.HACKER_GREEN}Watermark value: {bcolors.ENDC}" + watermark_values)    

         #print(watermark_values[0: 2]) # day
         #print(watermark_values[3: 5]) # month
         #print(watermark_values[6: 10]) # year    

         #print(watermark_values[11: 13]) # hours
         #print(watermark_values[14: 16]) # minutes
         #print(watermark_values[17: 19]) # seconds    


         day.append(watermark_values[0: 2])
         month.append(watermark_values[3: 5])
         year.append(watermark_values[6: 10])    

         hours.append(watermark_values[11: 13])
         minutes.append(watermark_values[14: 16])
         seconds.append(watermark_values[17: 19])    

         video_compatability.append('')    

         i += 1    

    except cv2.error as e:
         video_compatability.append('Corrupt')
         print(e)
         print('Bad file:', directory) # print out the names of corrupt files    


df = pd.DataFrame({'ROW': [], 'TREETAG': [], 'TREETAG_NOTES': [], 'FILEPATH': [], 
'FILENAME': [] , 'YEAR': [], 'MONTH': [], 'DAY':[], 'HH': [], 'MM': [], 'SS':[], 'Common':[], 
'SCIENTIFIC': [], 'QUANTITY': []})    

j = 0    

for file in all_video_dirs:
     try: 
          #if j < 10000:
          file_path = str(file)
          file_name = Path(file_path).stem
          #print(file_path)
          #print(file_name)
          for camera in cameras: 
               if camera in file_path: 
                    df = df.append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'YEAR': year[j], 'MONTH': month[j],
                                    'DAY': day[j], 'HH': hours[j], 'MM': minutes[j], 'SS': seconds[j], 'Common': video_compatability[j]}, ignore_index=True)       
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
              