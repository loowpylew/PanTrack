from asyncio.windows_events import NULL
import pytesseract
import cv2
from PIL import Image
import pandas as pd
import os, os.path
import sys
from pathlib import Path
import colorama 
import cv2
import msvcrt
import datetime


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
        

class Excel_Automation():
    def __init__(self): 
        self.temperature = []
        self.config = 'digits'        
        self.temperature = []
        self.day = []
        self.month = []
        self.year = []        
        self.hours = []
        self.minutes = []
        self.seconds = []        
        self.all_video_dirs = []        
        self.video_compatability = []        
        self.movement_detected_excel_input = []        
        self.year_comparison = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
                                '2011','2012','2013','2014','2015','2016','2017','2018','2019','2020',
                                '2021','2022','2023','2024','2025','2026','2027','2028','2029','2030',
                                '2031','2032','2033','2034','2035','2036','2037','2038','2039','2040']  # Maximum year (systhesised 
                                                                                                        # date) that will be compared 
                                                                                                        # with the watermark date.
                                                                                                        # Can be ammended to check
                                                                                                        # further dates within the 
                                                                                                        # future, but will slow 
                                                                                                        # down the runtime of the 
                                                                                                        # program if simply adding
                                                                                                        # onto existing list. 
                                                                                                        # Can be ammended to target
                                                                                                        # dates within a specific 
                                                                                                        # timeframe.      
        self.years = []        
        self.EXCEL_FILENAME = NULL        
        self.cameras = NULL        
        self.movement_detected = NULL        
        self.date_in_watermark = False        
        self.video_end_trigger = True
        self.sensitivity_value = 500 #px
        
        pytesseract.pytesseract.tesseract_cmd = Excel_Automation.resource_path("..\\Tesseract-OCR\\tesseract.exe")
        colorama.init()


    def clearConsole(): 
            command = 'clear'
            if os.name in ('nt', 'dos'): 
                command = 'cls'
            os.system(command)        

    
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS2
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    

    def print_ascci_art():
        print('''
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⡀⢄⠠⡠⡠⡠⡠⢠⠀⢄⢀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢄⣰⣤⣧⣷⣾⡾⡿⡿⡿⡿⡿⡿⡿⡿⡷⣷⣮⣦⣪⣐⠠⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⣢⣵⣾⣿⢟⢟⢝⢝⢎⣎⢎⢎⢎⢎⢎⢎⢎⢎⢎⢎⢎⢏⢯⢻⡻⣾⣦⣅⡂⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⣨⣾⣿⣟⢯⢣⣣⣷⣷⣷⣯⣷⣽⣽⣝⣝⢷⢧⢧⡣⡣⡣⡣⡣⡣⡣⡣⡫⡪⡪⡻⡿⣮⣔⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢐⣴⣿⡿⡻⡪⡪⡪⣷⣿⣿⣿⣿⣿⣿⣿⢿⢟⣟⢿⢽⣝⣝⣮⣮⢮⢮⣪⢪⢪⢪⢪⢪⢪⢪⢫⢻⢷⣮⡐⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⣴⣿⡿⡳⡹⣜⢜⡾⣽⣿⣿⣿⣿⣿⣟⢗⢵⣿⣟⢟⢟⢟⢿⣿⣟⢎⢧⡣⡫⡗⡕⡕⡕⡕⡕⡕⡕⡕⡝⡽⣿⣮⢐⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣨⣾⡿⣏⢎⢎⢎⢎⢮⣗⣿⣿⣿⣿⢿⢝⢎⢮⣿⡳⡱⡱⡱⡹⡎⣿⣞⣎⢎⢎⢯⡫⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⡻⣷⣔⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⣵⣿⡿⡹⡸⡱⡱⡱⡱⡱⣷⣿⣿⣟⢏⢧⡣⡣⡫⣿⡳⡹⣜⢜⢼⣹⣿⡝⡝⡝⣿⣿⡷⡕⡕⡕⡕⡕⡕⡕⡕⡕⡕⡕⡝⡞⣿⣮⠠⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⣽⣿⡟⣜⢜⢜⢜⢜⢜⢜⢜⢽⣮⡪⡪⡪⡪⡪⡪⡪⡺⣿⣮⣮⣮⡷⣟⣿⡝⣎⢎⣞⢞⣯⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢿⣧⠂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⣼⣿⣟⢜⢜⢮⢪⢪⢪⢪⢪⢪⢪⢪⢻⢺⢾⣮⣮⣪⡪⣮⣿⣿⢿⢿⢽⢾⣿⣿⣮⣧⣷⣿⣿⣷⣕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢝⢿⣧⢁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⢸⣿⣿⡸⡪⡪⡪⡳⡱⡱⡱⡱⡱⡱⡱⡱⡱⡱⡱⡹⡻⡻⡝⡕⡕⡕⡕⣵⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡕⡕⡕⡕⡕⡕⡕⡕⡕⡕⡕⡕⣝⣿⡆⢌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡂⣿⣿⣇⢗⢕⢕⢕⢕⢝⢜⢜⢜⢜⢜⢜⢜⢜⢜⢽⣿⣾⣮⣎⢎⢎⢎⢎⢎⢏⢏⢟⣿⡻⡻⣟⢟⢝⣎⢮⢮⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢺⣿⢀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⢸⣿⡿⡸⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⡪⣿⣿⣿⣿⣯⢧⡣⡣⡳⡵⡵⡵⡱⣵⡹⣮⡪⡻⣷⣹⣳⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢝⣿⡇⡐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢂⢽⣿⢯⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢷⣝⢿⡿⡿⡷⡝⡾⡼⡮⣮⡫⡪⡳⡹⣝⣕⢝⢮⡺⣜⢮⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢪⢾⣇⠂⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡂⣿⣿⣿⣿⠀⠠⠐⠈⡑⢕⢕⠕⠕⠕⢕⢕⠕⠕⡕⡕⡝⠝⠇⠀⠄⠄⠄⠄⠄⠄⠄⠀⠟⠟⠟⡿⣿⣟⠿⠝⠜⡕⡕⡕⠕⢕⠕⠕⡕⡕⢕⢕⢕⢕⢽⣗⠡⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢄⠠⢀⠄⠠⡀⠄⡠⢀⢂⠂⣿⣿⣿⡿⡄⢁⢘⡦⠐⠀⢧⠃⠄⠁⢘⢎⠠⢀⢹⢪⠂⡂⢵⡲⡲⡲⠀⡁⢰⢲⢲⠦⠨⢠⡁⠌⢻⡳⠀⠀⡂⢝⢎⠂⠔⡠⡂⠄⢝⠠⠀⡕⡕⡕⣽⣗⠡⢁⠢⢐⠠⠂⠄⡂⠄⠄⠄⠄
        ⠨⢐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠆⠠⢐⣟⠠⠁⡺⠀⢰⡁⠄⡳⠈⠀⠄⢳⠁⡂⢽⣿⣿⣯⠀⡂⢸⣿⣿⡇⠨⢐⠇⠠⢰⠅⠂⣕⠀⢸⠀⡂⢼⣾⡀⡂⠠⠠⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢈⢂
        ⠨⢐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠆⠐⠀⡁⠌⣠⠇⠌⠘⢂⢀⠪⢈⠰⡄⠂⠁⡂⢽⣿⣿⣗⠀⡂⢸⣿⣿⡇⠨⠀⢐⠠⣟⠠⠂⠓⢈⠐⡀⡂⢽⣷⡁⠄⡀⢊⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠐⠄
        ⠨⢐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠅⢁⣤⣶⣯⢁⠂⣦⡦⠀⡈⠠⠐⣿⡄⠡⡂⢽⣿⣿⣗⠀⡂⠸⣿⣿⡇⠨⢰⡀⠀⡃⠔⢰⣴⠄⡀⢢⠀⠌⠚⠄⠅⢪⡀⠄⠹⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠨⡈
        ⠌⡐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠁⢐⣿⣿⣷⣤⣦⣿⣯⣦⣤⣤⣤⣿⣿⣤⣤⣺⣿⣿⣗⠀⠀⢘⣿⣿⣧⣤⣴⣷⣤⣦⣴⣼⣿⣥⣤⣼⣶⣄⣴⣦⣴⣼⣷⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠐⠄
        ⢂⠌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢈⠂
        ⠡⠁⠂⠅⠂⠅⠂⠅⠂⠅⠂⠅⠂⠅⠂⠅⠂⠅⠂⠅⢂⠝⢿⣿⣷⣵⣱⢱⡱⡕⣕⢵⢷⡵⣱⡵⡕⣵⣱⢵⢱⢱⢱⢵⢧⣇⢇⡷⣕⢕⢕⢕⢕⢕⢕⣵⣿⢿⢙⠨⠐⠨⠐⠨⠐⠨⠐⠨⠐⠨⠐⠨⠐⠨⠐⠨⠐⠐⠄⠅
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠠⢑⠻⡿⣿⣿⣿⣯⣺⢺⣳⡽⡽⡯⣯⣺⡯⣯⣻⣿⣽⢽⢽⢽⡱⣯⣗⢧⣳⣷⣵⣿⢿⠻⠩⢐⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠐⠨⢘⠹⠻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣽⣿⣿⣿⣿⣿⢿⠟⠟⡨⠂⠌⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⢊⠌⡙⡙⠟⢟⠿⡿⡿⣿⣿⣿⣿⢿⢿⢟⠟⢟⢋⠫⡈⡂⠅⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠁⠂⠌⠐⠨⠀⡂⢂⠂⠅⠂⠢⠈⠐⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ''')            

    def user_interface(self): 
        Excel_Automation.clearConsole()    

        #print("--------------------------Excel input automation - [Animal Classification]-------------------------")    

        Excel_Automation.print_ascci_art()
        print("---------------------------------------------------------------------------------------------------")
        print(f"| - {bcolors.HACKER_GREEN}To process all videos, you will be required to enter the directory path in which{bcolors.ENDC}              |")
        print(f"|   {bcolors.HACKER_GREEN}all cameras our housed.{bcolors.ENDC}                                                                       |") 
        print(f"|   (Copyright: Lewis Taylor, Liam Taylor)                                                        |") 
        print("---------------------------------------------------------------------------------------------------")            

        print(f"{bcolors.HACKER_GREEN}For further details as to what this script does, please enter '{bcolors.ENDC}y{bcolors.HACKER_GREEN}', otherwise enter '{bcolors.ENDC}q{bcolors.HACKER_GREEN}' to continue: {bcolors.ENDC}")            

        place_holder = True
        while place_holder: 
             val = input().lower()
             if val == 'q': 
                  break 
             elif val == 'y': 
                print("""\n        - Optimal Character Recognition has been used within this script to identify the watermarked dates upon creation of 
          a video as result of the camera being triggered by sudden movements.
          
        - The time span of each video is around 1 - 2 minutes.        

        - The software has to process the file directory to where an individual video is housed, the file name of the video, 
          the watermark date/time and temperature within the video (recorded by the video camera, sensors etc), whether the 
          videos are corrupt or not and whether there is movement within the video (preferably an animal) so that the user of 
          the software is only required to watch videos with animal species in (can classify animal species) as opposed to
          watching thousands of videos where no animal activity takes place. All this information is then automatically
          loaded within an excel spreadsheet which can then be further analysed by users using a programming language such as
          a ‘R’, SPSS (data inputter) or python (same language used to develop this software) to perform statical models on 
          the data generated. This will save 100’s of hours of tedious identifying and inputting data as described above row
          by row, column by column within the excel spreadsheet.        

        - If the 60 second indicator ('60s') appears within a video, this will automatically trigger the movement detection 
          software into thinking something has moved due to the sudden differences in frames.         

        - The following columns will be manipulated:         

          '' - This will contain the index of each row, this is an automatic response by the ExcelWriter() function which is 
               used to write all data captured to the specified excel spreadsheet.         

          'ROW'  - This column will remain empty (outside the scope of this software's purpose).        

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

          'QUANTITY' - This column will contain either: 
                     
                     - '0.0' to indicate no animal species have been identified i.e. file is 'Corrupt' or
                        no movement was detected
                    
           """)
                 
                while True: 
                    print(f"\n{bcolors.HACKER_GREEN}Please enter '{bcolors.ENDC}q{bcolors.HACKER_GREEN}' to continue to enter directory path: {bcolors.ENDC}")
                    val = input().lower()
                    if val == 'q': 
                         place_holder = False
                         Excel_Automation.clearConsole()
                         break
                    else: 
                        Excel_Automation.clearConsole()
                        Excel_Automation.print_ascci_art()
                        continue
             else: 
                  Excel_Automation.clearConsole()
                  Excel_Automation.print_ascci_art()
                  print(f"{bcolors.HACKER_GREEN}Please enter '{bcolors.ENDC}y{bcolors.HACKER_GREEN}', otherwise enter '{bcolors.ENDC}q{bcolors.HACKER_GREEN}' to continue: {bcolors.ENDC}")            

        while(1): 
            try:
                Excel_Automation.clearConsole()
                Excel_Automation.print_ascci_art()
                print(f"\n{bcolors.HACKER_GREEN}Please enter Directory PATH: {bcolors.ENDC}", end="")
                DIR = input()
                directory_contents = os.listdir(DIR)
                break
            except: 
                while(1): 
                    Excel_Automation.clearConsole()
                    Excel_Automation.print_ascci_art()
                    print(f"{bcolors.ENDC}[{bcolors.HACKER_GREEN}The directroy path entered does not exist{bcolors.ENDC}]")
                    print(f"{bcolors.HACKER_GREEN}Please enter '{bcolors.ENDC}y{bcolors.HACKER_GREEN}' to re-enter an existing directory, otherwise press '{bcolors.ENDC}q{bcolors.HACKER_GREEN}' to end the program:{bcolors.ENDC}")
                    val = input().lower() 
                    if val == 'y': 
                        Excel_Automation.clearConsole()
                        break 
                    elif val == 'q': 
                        exit() 
                    else:
                        Excel_Automation.clearConsole()
                        continue        

        year_count = 0
        existing_year_count = 0
        flag = True
        alr_ins = True
        do_not_append = True    
    

        Excel_Automation.clearConsole()
        Excel_Automation.print_ascci_art()
        print(f"\n{bcolors.HACKER_GREEN}Years to select from: {bcolors.ENDC}", self.year_comparison)
        print(f"\n{bcolors.HACKER_GREEN}Specifying specfic years in videos will speed up processing of software{bcolors.ENDC}.")
        print(f"{bcolors.HACKER_GREEN}If all years are not known, will not impede on the ability to process videos that are available{bcolors.ENDC}.")
        print(f"\n{bcolors.HACKER_GREEN}Please enter the year/years video's fall into ({bcolors.ENDC}i.e. 2022{bcolors.HACKER_GREEN}):{bcolors.ENDC}", end=" ")
        year_input = input() 
        while(1): 
            try:
                if flag == False: 
                    break 
                else:
                    for year in self.year_comparison: 
                        year_count += 1
                        if year == year_input: 
                            for year in self.years:
                                existing_year_count += 1
                                if year == year_input:
                                    while(1):
                                        Excel_Automation.clearConsole()
                                        Excel_Automation.print_ascci_art()
                                        print(f"\n{bcolors.HACKER_GREEN}Year has already been added to system", end=" ")
                                        print(f"\n{bcolors.HACKER_GREEN}If you would like to enter another date press '{bcolors.ENDC}y{bcolors.HACKER_GREEN}' otherwise press '{bcolors.ENDC}n{bcolors.HACKER_GREEN}':{bcolors.ENDC}", end=" ")
                                        val = input().lower() 
                                        Excel_Automation.clearConsole()
                                        if val == 'y': 
                                            do_not_append = False
                                            break
                                        elif val == 'n':
                                            alr_ins = False
                                            break
                                else: 
                                    pass    

                            if alr_ins == False: 
                                flag = False
                                break     

                            elif existing_year_count == len(self.years) and do_not_append == True: 
                                existing_year_count = 0
                                self.years.append(year_input)
                                while(1):
                                    Excel_Automation.clearConsole()
                                    Excel_Automation.print_ascci_art()
                                    print(f"\n{bcolors.HACKER_GREEN}Years added to system: {bcolors.ENDC}", self.years, end=" ")
                                    print(f"\n{bcolors.HACKER_GREEN}If you would like to include another date, press '{bcolors.ENDC}y{bcolors.HACKER_GREEN}' otherwise press '{bcolors.ENDC}n{bcolors.HACKER_GREEN}':{bcolors.ENDC}", end=" ")
                                    val = input().lower() 
                                    Excel_Automation.clearConsole()
                                    if val == 'y':     
                                        break
                                    elif val == 'n':
                                        flag = False
                                        break    

                        elif year_count == (len(self.year_comparison) + 1) and flag != False:
                            year_count = 0
                            existing_year_count = 0
                            do_not_append = True
                            Excel_Automation.clearConsole()
                            Excel_Automation.print_ascci_art()
                            print(f"\n{bcolors.HACKER_GREEN}Years to select from: {bcolors.ENDC}", self.year_comparison)
                            print(f"\n{bcolors.HACKER_GREEN}Please enter an existing year video's fall into ({bcolors.ENDC}i.e. 2022{bcolors.HACKER_GREEN}):{bcolors.ENDC}", end=" ")
                            year_input = input() 
                        else:
                            continue 
            except: 
                break        

        Excel_Automation.clearConsole()
        Excel_Automation.print_ascci_art()
        print(f"{bcolors.HACKER_GREEN}\nPlease enter the excel file name to which you wish the data to be uploaded to{bcolors.ENDC}.")
        print(f"({bcolors.FAIL}Note:{bcolors.ENDC} Please have Microsoft Excel closed otherwise program will not succefully output to spreadsheet{bcolors.ENDC}):")
        while(1):
             EXCEL_FILENAME = input()
             if len(EXCEL_FILENAME) >= 6 and ".xlsx" in EXCEL_FILENAME:
                  Excel_Automation.clearConsole()
                  break
             elif len(EXCEL_FILENAME) >= 6 and ".xlsx" not in EXCEL_FILENAME:
                  Excel_Automation.clearConsole()
                  Excel_Automation.print_ascci_art()
                  print(f"{bcolors.HACKER_GREEN}Please enter excel filename including the '{bcolors.ENDC}.xlsx{bcolors.HACKER_GREEN}' extension: {bcolors.ENDC}")
                  continue
             elif len(EXCEL_FILENAME) < 6:
                  Excel_Automation.clearConsole()
                  Excel_Automation.print_ascci_art()
                  print(f"{bcolors.HACKER_GREEN}Please enter excel filename including the '{bcolors.ENDC}.xlsx{bcolors.HACKER_GREEN}' extension: {bcolors.ENDC}")
                  continue 
             
     
        while(1):
            Excel_Automation.clearConsole()
            Excel_Automation.print_ascci_art()
            print(f"To Note: - {bcolors.HACKER_GREEN}Used to enhance the sensitivity when detecting movement within videos.") 
            print(f"{bcolors.ENDC}         - {bcolors.HACKER_GREEN} Sensitivity currently preset to 500px (px - pixels){bcolors.ENDC}.")
            print(f"{bcolors.ENDC}         - {bcolors.HACKER_GREEN} Minumum suggested sensitivity: 500px (do not include px - unit of measure){bcolors.ENDC}.")                                     
            print(f"{bcolors.HACKER_GREEN}\nPlease enter sensitivity value if you wish to change (measured in pixels {bcolors.ENDC}'px'{bcolors.HACKER_GREEN}), otherwise, press {bcolors.ENDC}'q'{bcolors.HACKER_GREEN} : {bcolors.ENDC}")    

            val = input()
            if val == 'q'.lower(): 
                Excel_Automation.clearConsole()
                break    

            # if the value entered cannot be casted to a float, it means the value passed is not a number thus will be caught in a try catch. Otherwise, the while loop is broken. 
            try: 
                to_int = int(val)
                
                if to_int <= 500: 
                    pass
                else: 
                    self.sensitivity_value = to_int
                    del to_int # removes reference to variable as will not be used elsewhere within the program. 
                               # Removes redundency. 
                    Excel_Automation.clearConsole()
                    break       
            except: 
                pass    
    

        while(1): 
             Excel_Automation.clearConsole()
             Excel_Automation.print_ascci_art()
             print(f"\n{bcolors.HACKER_GREEN}Video movement detection viewer will automatically run while processing. If you would like to remove this function, enter '{bcolors.ENDC}y{bcolors.HACKER_GREEN}' otherwise, enter '{bcolors.ENDC}q{bcolors.HACKER_GREEN}'{bcolors.ENDC}.")
             print(f"({bcolors.FAIL}Note:{bcolors.ENDC} Removal of video movement detection viewer may increase processing speed by up to 15% - 20%{bcolors.ENDC}):")
             val = input()
             if val == 'q'.lower(): 
                output_video_frames = True
                Excel_Automation.clearConsole()
                break 
             elif val == 'y'.lower(): 
                 output_video_frames = False
                 Excel_Automation.clearConsole()
                 break
             else: 
                continue        

        Excel_Automation.print_ascci_art()

        print(f"\n{bcolors.HACKER_GREEN}Video cameras to be processed: {bcolors.ENDC}" + str(directory_contents) + "\n")            

        cameras = directory_contents          

        i = 0    

        for root, dirs, files in os.walk(DIR): 
            for file in files:
                # Filter out files starting with "._" -  indicates that the folder has been accessed or copied from a Mac system to a non-Mac system. These files are resource forks or metadata files created by macOS.
                #if not file.startswith("._"):
                if file.endswith('.AVI') or file.endswith('.MP4'): 
                    self.all_video_dirs.append(os.path.join(root, file))  
                    i += 1  
                #else: 
                    #continue    
    
        print(f"\n{bcolors.HACKER_GREEN}Number of videos to be processed: {bcolors.ENDC}" + str(i) + "\n")     

        return self.years, cameras, output_video_frames, EXCEL_FILENAME    
            

    def movement_Detection(self, cap, out, i, count, ret, frame1, frame2, movement_detected, video_end_trigger, output_video_frames): 
        while cap.isOpened():
            # Without this condition: 'ret == False', the software will pause until the program has been forcefully ended.
            # The reason for the error is due to the video cap ending, and cv2 still trying to capture it even after the end.
            # hence this will break the processing of the current video so that the next video inline can be processed. 
            if ret == False:
                break        

            diff = cv2.absdiff(frame1, frame2) # difference between both frames.
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # convert to gray scale, helps discover contours. 
            blur = cv2.GaussianBlur(gray, (5,5), 0) # blur gray scale frame, (5,5) - kernel size, sigma value.
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3) # fills in holes to discover better contours.
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)        

            temp_diff_frame_blocker = 0
            
            ###################################### SENSITIVITY CAN BE SET HERE ########################################
            # To Note: used to minimise tradeoff between videos with animals not being detected when their are animals 
            #          within videos and movement being detected when there are no animals in video. 
            for contour in contours:
                (x, y, width, height) = cv2.boundingRect(contour)    
                if cv2.contourArea(contour) < self.sensitivity_value:  # Sensitivity currently preset to 500px (px - pixels).
                                                                       # Minumum suggested sensitivity: 500px (do not include px - unit of measure)
                                                                       # Only adjust numerical figure in this section to enhance the sensitivity 
                   continue
            ###########################################################################################################
                
                # roi - region of image
                roi = frame1[y:y+height, x:x+width]        

                cv2.imwrite(Excel_Automation.resource_path("..\\images\\frames\\roi.jpg"), roi)        

                image = cv2.imread(Excel_Automation.resource_path("..\\images\\frames\\roi.jpg"))        

                img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)             

                watermark_values_ROI = pytesseract.image_to_string(img_RGB, config ='--psm 4')     
                    

                if watermark_values_ROI[0:3] == '60S':
                       
                       temp_diff_frame_blocker += 1
                               

                if diff.any() == True and temp_diff_frame_blocker != 1:
                   if count == 1: 
                       movement_detected = "Yes"
                       self.movement_detected_excel_input[i] = ""
                       video_end_trigger = False
                       
                   count += 1        

                   temp_diff_frame_blocker = 0         

                if output_video_frames == True: 
                    cv2.rectangle(frame1, (x, y), (x+width, y+height), (0, 255, 0), 2)
                    cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 3)        

            if output_video_frames == True: 
           
                cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)            

                temporary_resize = cv2.resize(frame1,(1000,500),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                cv2.imshow("Movement Detection", temporary_resize)               

            frame1 = frame2
            ret, frame2 = cap.read()        

            if video_end_trigger == False: 
               video_end_trigger = True
               break 
              
            cv2.waitKey(1)        

        cap.release()
        out.release()        

        return movement_detected        

        # The date checker function was created to have some form of marker to compare against/authenticate
        # so that the output (watermark information) is formatted correctly.         

    def date_checker(self, watermark_date, month_hold, day_hold, year_hold, years): 
        days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 
                            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
                            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']        

        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']    
    

        complete_date = month_hold + day_hold + year_hold # Without semi-colons to seperate day, month and year.
         
        day_count = 0 
        month_count = 0 
        year_count = 0    
     
        while(1):
            possible_date = days[day_count] + months[month_count] + years[year_count]
            
            day_count += 1
            
            # Possible date and complete date are concentanted in reverse order given 
            # the use of American/style format of dates in watermark frames. 
            # The arrays that hold a snippet of a possible date have been concentatnated using
            # the English date format as written in Great Britian. 
            if complete_date == possible_date: 
                 watermark_date = True 
                 break
            else: 
                 if day_count == 31:
                      month_count += 1
                      if month_count == 12: 
                           year_count += 1
                           if year_count == len(years):
                                if day_count == 31 and month_count == 12: 
                                     day_count = 0 
                                     month_count = 0 
                                     year_count = 0
                                     break 
                           
                           month_count = 0       
                      day_count = 0 
     
        return watermark_date
        
                             
    def watermark_processing(self, i, READING, INDEX, TEST_VID, directory, movement_detected, years):
        while READING:
            TEST_VID.set(1, INDEX)
            READING, IMG = TEST_VID.read()
            RET, FRAME = TEST_VID.read()               

            NAME = Excel_Automation.resource_path("..\\images\\frames\\watermark_snippet.jpg")            

            cv2.imwrite(NAME, FRAME)            

            im = Image.open(NAME)            

            # All params below are measured in pixels (px)
            if directory.endswith('.MP4'): 
                # For both .AVI and .MP4 video files, there are some files where the stamp that houses the watermark 
                # along with the temperature have a larger width and height, thus the image generated as a result of
                # saving the first frame of each video will not display the section where the watermark is housed. 
                # This section is used to isolate the temperature, date and time so that we can perform Optimal Character Recognition.
                # We are able to store the temperature, date and times in order to further plot within an excel spreadsheet. 
                # Thus, we have to re-specify the dimensions of the image generated that we want to isolate in order to perform
                # successful OCR. 
                # As of the time of writing (2023), the videos supplied have 1 of 3 stamp sizings within the videos. 
                # Where the output will result in one of the following: 
                # - being equal to an empty string 
                # - being equal to a string containing something, but not a date that matches with a sythesised date
                # - a string that matches with a sythesised date. 
               
                
                # Width: 1920
                # Height: 1080
                left = 725 # Begins at 0 for left up to maxiumum width of image 
                top = 1050 # Begins at 0 up to maxiumum height of image
                right = 1905 # Will exclude everything from and up to the maximum width
                bottom = 1080 # Will exclude everything from and up to the maximum height"""            

                imc = im.crop((left, top, right, bottom))
                imc.save(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))    

                image = cv2.imread(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))
                img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # pytesseract API only accepts image in RGB format      
                                                                 # Tesseract options for txt format styles found within images: https://muthu.co/all-tesseract-ocr-options/
                                                                 # Known as page segmentation (option 6: Assume a single uniform block of text)    
                watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')          

                # A large percentage of watermarks within videos with .mp4 file extention fall witin these dimensions       

                print(watermark_values)          

                day_holder = watermark_values[9:11]
                month_holder = watermark_values[12:14]
                year_holder = watermark_values[15:19]    

                print(day_holder)
                print(month_holder)
                print(year_holder)    

                if Excel_Automation.date_checker(self, self.date_in_watermark, month_holder, day_holder, year_holder, years) != True:
                    if watermark_values != '': 
                        #print("watermark_values != ''")
                        # Width: 1920 
                        # Height: 1080
                        left = 725  
                        top = 1050 
                        right = 1905 
                        bottom = 1080           

                        imc = im.crop((left, top, right, bottom))
                        imc.save(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))        

                        image = cv2.imread(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))
                        img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      
                           
                        watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')                 

                        #self.temperature.append(watermark_values[0:8])
                        #self.day.append(watermark_values[8:10])
                        #self.month.append(watermark_values[11:13])
                        #self.year.append(watermark_values[14:18])            

                        #self.hours.append(watermark_values[19:21])
                        #self.minutes.append(watermark_values[22:24])
                        #self.seconds.append(watermark_values[25:27])    

                        self.temperature.append(watermark_values[0:8])
                        self.day.append(watermark_values[9:12])
                        self.month.append(watermark_values[13:15])
                        self.year.append(watermark_values[16:20])            

                        self.hours.append(watermark_values[21:23])
                        self.minutes.append(watermark_values[24:26])
                        self.seconds.append(watermark_values[27:29]) 
                    else:
                        #print("watermark_values == ''")
                        # Width: 1280
                        # Height: 720
                        left = 425
                        top = 675
                        right = 1270
                        bottom = 720             

                        imc = im.crop((left, top, right, bottom))
                        imc.save(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))            

                        image = cv2.imread(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))
                        img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)             

                        watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')            

                        self.temperature.append(watermark_values[0:9])
                        self.day.append(watermark_values[10:12])
                        self.month.append(watermark_values[13:15])
                        self.year.append(watermark_values[16:20])    
                        self.hours.append(watermark_values[21:23])
                        self.minutes.append(watermark_values[24:26])
                        self.seconds.append(watermark_values[27:29])        

                else:
                   #print("Match: date exists")
                   # We only append once date in watermark has been checked. 
                   self.temperature.append(watermark_values[0:8])
                   self.day.append(watermark_values[9:11])
                   self.month.append(watermark_values[12:14])
                   self.year.append(watermark_values[15:19])            

                   self.hours.append(watermark_values[20:22])
                   self.minutes.append(watermark_values[23:25])
                   self.seconds.append(watermark_values[26:28])        

            elif directory.endswith('.AVI'):
                # Width: 1280
                # Height: 720
                left = 800 
                top = 690 
                right = 1280 
                bottom = 720         

                imc = im.crop((left, top, right, bottom))
                imc.save(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))     

                image = cv2.imread(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))
                img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      
                 
                watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')      
                
                # Not too sure why i used these indexes, but commented out for future reference/development
                #day_holder = watermark_values[9:11]
                #month_holder = watermark_values[12:14]
                #year_holder = watermark_values[15:19]  
                
                # Edited so that the day and month are allocated to the correct array. 
                # Day and month are in reverse order. 
                day_holder = watermark_values[3:5]  
                month_holder = watermark_values[0:2]
                year_holder = watermark_values[6:10]    
    

                #print(day_holder)
                #print(month_holder)
                #print(year_holder)    

                if Excel_Automation.date_checker(self, self.date_in_watermark, month_holder, day_holder, year_holder, years) != True:
                    if watermark_values != '':
                        #print("watermark_values != ''")
                        # Width: 1280 
                        # Height: 720
                        left = 800 
                        top = 690 
                        right = 1280 
                        bottom = 720         

                        imc = im.crop((left, top, right, bottom))
                        imc.save(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))     

                        image = cv2.imread(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))
                        img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
           
                        watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6')           

                        #print(watermark_values)
                        #print(watermark_values[0:2])
                        #print(watermark_values[3:5])
                        
                        self.temperature.append('')
                        #self.day.append(watermark_values[0:2])
                        #self.month.append(watermark_values[3:5])    

                        self.month.append(watermark_values[0:2])
                        self.day.append(watermark_values[3:5])
                        self.year.append(watermark_values[6:10])            

                        self.hours.append(watermark_values[11:13])
                        self.minutes.append(watermark_values[14:16])
                        self.seconds.append(watermark_values[17:19])
                    else: 
                        #print("watermark_values == ''")    
                        # Width: 1250 
                        # Height: 720 
                        left = 850 
                        top = 675 
                        right = 1250 
                        bottom = 720             

                        imc = im.crop((left, top, right, bottom))
                        imc.save(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))            

                        image = cv2.imread(Excel_Automation.resource_path("..\\images\\frames\\generated_frame.jpg"))
                        img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)             

                        watermark_values = pytesseract.image_to_string(img_RGB, config ='--psm 6') 
                else: 
                    #print("Match: date exists")
                    self.temperature.append('')
                    #self.day.append(watermark_values[0:2])
                    #self.month.append(watermark_values[3:5])    

                    # Edited so that the day and month are allocated to the correct array. 
                    # Day and month are in reverse order. 
                    self.month.append(watermark_values[0:2])
                    self.day.append(watermark_values[3:5])
                    self.year.append(watermark_values[6:10])            

                    self.hours.append(watermark_values[11:13])
                    self.minutes.append(watermark_values[14:16])
                    self.seconds.append(watermark_values[17:19])        

            else: 
                print("Not an AVI/MP4 file")
                pass            

            break # ends looping through frames             

        print("\n")
        print("   ⣃⣮⣾⣵⣷⣓⣷⣬⣊       -----------------------------------------------------------------------------")
        print(" ⢀⣞⣿⣿⣿⡿⠿⣻⣿⣮⣯⡷⠖⠧⡌   " + f"{bcolors.HACKER_GREEN}Video Number: {bcolors.ENDC}" + str(i))
        print(" ⣺⣿⣿⣿⠟⠁⣿⠃⠀⢠⢹⣇⠀⢰⠃   " + f"{bcolors.HACKER_GREEN}Directory name: {bcolors.ENDC}" + directory) 
        print(" ⢺⡿⠟⠁⠀⠀⢿⡀⠀⢌⣿⠉⠙⣻⡇   " + f"{bcolors.HACKER_GREEN}Watermark value: {bcolors.ENDC}" + watermark_values, end="")
        print(" ⠳⠤⣤⣀⡀⣸⣿⣿⣯⣿⣧⣀⣷⣷⣄   " + f"{bcolors.HACKER_GREEN}Movement detected: {bcolors.ENDC}" + movement_detected)
        print("   ⢠⣉⠛⠉⠁⠀⢰⣿⣿⣿⣿⣿⠿⠧  -----------------------------------------------------------------------------")
        print("   ⣿⣿⣧⠀⠀⣀⢀⢩⡁⡍⢤⢶⡉")
        print("   ⠘⢯⣿⣿⣆⢲⣦⣬⣘⣬⣡⣜⣬⡔")
        print("     ⠈⠿⠿⠿⠿⠿⢿⣿⣿⣿⠿")
    

    def excel_data_inputter(self, cameras, excel_filename, start_time): 
        df = pd.DataFrame({'ROW': [], 'TREETAG': [], 'TREETAG_NOTES': [], 'FILEPATH': [], 
                           'FILENAME': [] , 'TEMPERATURE': [], 'YEAR': [], 'MONTH': [], 'DAY':[], 'HH': [], 'MM': [], 'SS':[], 'Common':[], 
                           'SCIENTIFIC': [], 'QUANTITY': []})    
        j = 0            

        i = 0 # Used to prevent overlapping of data held in arrays i.e. year, month, day etc...
              # Doesn't affect indexing of 'j' where data is actually held.
        print("\n")
        print(f"{bcolors.WARNING}NOTIFICATION:")
        print(F"{bcolors.ENDC}In order to populate your spreadsheet, you will now have to close any excel sheets you have open.")
        print("Press any key to continue...")
        
        while(1): 
            if msvcrt.kbhit():
                key = msvcrt.getch()
                break
        
        print("\n")    

        for file in self.all_video_dirs:
            #try: 
                file_path = str(file)
                file_name = Path(file_path).stem
                print(file_path)
                
                for camera in cameras: 
                     if camera in file_path: 
                        if self.video_compatability[i] == "Corrupt":
                            df = df._append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'Common': 'Corrupt'}, ignore_index=True)
                        elif file_path.endswith('.MP4'):
                            if self.movement_detected_excel_input[j] == "":
                               df = df._append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'TEMPERATURE': self.temperature[j], 'YEAR': self.year[j], 'MONTH': self.month[j],
                                            'DAY': self.day[j], 'HH': self.hours[j], 'MM': self.minutes[j], 'SS': self.seconds[j], 'Common': self.movement_detected_excel_input[j]}, ignore_index=True)
                            elif self.movement_detected_excel_input[j] == "None": 
                                df = df._append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'TEMPERATURE': self.temperature[j], 'YEAR': self.year[j], 'MONTH': self.month[j],
                                            'DAY': self.day[j], 'HH': self.hours[j], 'MM': self.minutes[j], 'SS': self.seconds[j], 'Common': self.movement_detected_excel_input[j], 'QUANTITY': 0}, ignore_index=True)
                            j += 1 
                        elif file_path.endswith('.AVI'):  
                           if self.movement_detected_excel_input[j] == "":
                               df = df._append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'TEMPERATURE': '', 'YEAR': self.year[j], 'MONTH': self.month[j],
                                             'DAY': self.day[j], 'HH': self.hours[j], 'MM': self.minutes[j], 'SS': self.seconds[j], 'Common': self.movement_detected_excel_input[j]}, ignore_index=True)
                           elif self.movement_detected_excel_input[j] == "None":
                               df = df._append({'TREETAG': camera, 'FILEPATH': file, 'FILENAME': file_name, 'TEMPERATURE': '', 'YEAR': self.year[j], 'MONTH': self.month[j],
                                             'DAY': self.day[j], 'HH': self.hours[j], 'MM': self.minutes[j], 'SS': self.seconds[j], 'Common': self.movement_detected_excel_input[j], 'QUANTITY': 0}, ignore_index=True) 
                           j += 1  
                         
                        i += 1 # Increment i for "Corrupt" row    

            #except:
            #    print(f"[{bcolors.HACKER_GREEN}Exception Handled: {bcolors.ENDC}Index out of bounds{bcolors.ENDC}]")
        
        print(df)            

        #print(i)
        #print(self.video_compatability)    

       
        # Define the output file path, overwriting if it already exists
        output_path =  Excel_Automation.resource_path(f'..\\pantrack_output_files\\{excel_filename}')

        datatoexcel = pd.ExcelWriter(output_path) # engine="xlsxwriter"            

        df.to_excel(datatoexcel, sheet_name='video_data', index=False, na_rep='', freeze_panes=(1, 1))
        
        # datatoexcel.freeze_panes(1,1) # Freezes top row and/or column when exporting a pandas DataFrame to Excel        

        # Auto-adjust columns' width
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            datatoexcel.sheets['video_data'].set_column(col_idx, col_idx, column_width)
        
        datatoexcel.close()

        end_time = datetime.datetime.now()
        total_time = end_time - start_time    

        print(f''' 
    ⣃⣮⣾⣵⣷⣓⣷⣬⣊
 ⢀⣞⣿⣿⣿⡿⠿⣻⣿⣮⣯⡷⠖⠧⡌
 ⣺⣿⣿⣿⠟⠁⣿⠃⠀⢠⢹⣇⠀⢰⠃⠀⠀
 ⢺⡿⠟⠁⠀⠀⢿⡀⠀⢌⣿⠉⠙⣻⡇⠀⠀⠀⠀
 ⠀⠳⠤⣤⣀⡀⣸⣿⣿⣯⣿⣧⣀⣷⣷⣄⠀⠀⠀
 ⠀⠀⠀⢠⣉⠛⠉⠁⠀⢰⣿⣿⣿⣿⣿⠿⠧⠀⠀
 ⠀⠀⠀⢸⣿⣿⣧⠀⠀⣀⢀⢩⡁⡍⢤⢶⡉⠀⠀[{bcolors.HACKER_GREEN}End of processing{bcolors.ENDC}]
 ⠀⠀⠀⠘⢯⣿⣿⣆⢲⣦⣬⣘⣬⣡⣜⣬⡔⠀⠀Total execution time: , {total_time}
 ⠀⠀⠀⠀⠀⠈⠿⠿⠿⠿⠿⢿⣿⣿⣿⠿⠀⠀                                                                                             
       ''')
        print("\n")
        print("Press any key to exit the program...")
     
    while(1): 
        if msvcrt.kbhit():
            key = msvcrt.getch()
            break