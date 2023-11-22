from excel_automation import Excel_Automation 
from excel_automation import bcolors
import datetime
import cv2

def run_all_processes():

    ea = Excel_Automation() # Initialization of variables required to store video data 
                            # and other variables that require intial values to be set
                            # before runtime of watermark processing and movement detcetion.
     
    years, cameras, output_video_frames, excel_filename = ea.user_interface() 
    
    i = 0    
        
    start_time = datetime.datetime.now()
    
    for files in ea.all_video_dirs: 
        directory = str(files) 
        try:
            # Video URL
            TEST_VID = cv2.VideoCapture(directory)
            cap = cv2.VideoCapture(directory)
            READING, IMG = cap.read()            

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi',fourcc, 5, (1280,720))

            ret, frame1 = cap.read()
            ret, frame2 = cap.read()   
                
            # Frame Number - used to grab first frame of every video processed to capture watermark information
            INDEX = 0
             
            count = 0      

            video_end_trigger = True   

            movement_detected = "No"

            ea.movement_detected_excel_input.append("None")   
             
            movement_detected = ea.movement_Detection(cap, out, i, count, ret, frame1, frame2, movement_detected, video_end_trigger, output_video_frames)
             
            ea.watermark_processing(i, READING, INDEX, TEST_VID, directory, movement_detected, years) 
             
            ea.video_compatability.append('')

        except cv2.error:
            ea.video_compatability.append("Corrupt")
            print(f'{bcolors.WARNING}Bad file:{bcolors.ENDC} ', directory) # print out the names of corrupt files
            print(f'{bcolors.OKBLUE}Causation: {bcolors.ENDC}Video cannot be opened, no known reason as to why it is corrupt')
        except KeyboardInterrupt: 
            exit() # will exit the program causing a runtime error to occur which will be caught within the main loop
        except: 
            ea.video_compatability.append("Corrupt")
            print(f'{bcolors.WARNING}Bad file:{bcolors.ENDC} Moov atom is never added to the end of file, thus is unopenable.')
            print(f'{bcolors.OKBLUE}Causation:{bcolors.ENDC} Video camera adruptly stopped recording thus stopped in the middle of')
            print(f'the encoding of the video') 
        
        i += 1
            
    ea.excel_data_inputter(cameras, excel_filename)

    #print(ea.video_compatability)
     
    end_time = datetime.datetime.now()
    total_time = end_time - start_time    
    print("Total execution time:", total_time)
    

if __name__ == '__main__':
    try:
        run_all_processes()
    except:
        print(f"\n{bcolors.FAIL}KeyboardInterrupt {bcolors.ENDC}'Ctrl c' {bcolors.FAIL}has been entered")
        print(f"Program adruptly ended{bcolors.ENDC}.")