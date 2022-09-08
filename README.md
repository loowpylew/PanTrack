# Animal_classification_system

Copyrighted by Lewis Taylor

In order to run this software, you will be requested by the terminal upon running the excel_automation.py file to install various modules which are used by the software to call specific functions i.e. pip install opencv-python , a module used to read the txt within an image/video file. 

You can search up the pip command for a specific module requested by the terminal using the following link: https://pypi.org/.

How to install pip for windows (used to install python modules):

https://phoenixnap.com/kb/install-pip-windows

You will also need to open the file up with python. This will require you to download the python compiler. You can 
download the latest version from: https://www.python.org/downloads/

You will also be required to install the tesseract python distribution to perform optimal character recognotion (early machine learning technique used to decipher text within images). 

Tesseract download page: https://tesseract-ocr.github.io/tessdoc/Downloads.html 

Direct link to both 32 and 64 bit .exe file extensions for tesseract: https://github.com/UB-Mannheim/tesseract/wiki

Here, we download the third party .exe file extensions for windows. By default, when installed, 
the API's associated files can be found in program files within your PC's file system. 

To install the tesseract python distribution, type the following in the terminal: 
pip install pytesseract 

- Optimal Character Recognition has been used within this script to identify the watermarked dates upon creation of 
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

     Beginning of processing:
    
     ![image](https://user-images.githubusercontent.com/65728188/189197015-9a32f172-2cf3-43b0-b025-949a18474058.png)

     Cameras being processed: 
   
     ![image](https://user-images.githubusercontent.com/65728188/189197192-0d005c91-2d51-4003-879e-195c9fab3a27.png)

     Movement detection visual display: 
     
     ![image](https://user-images.githubusercontent.com/65728188/189197318-4e5ea4db-d04c-47b0-bff2-4d4ff84315a1.png)

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

      'QUANTITY' - This column will contain either: 
                 
                 - '0.0' to indicate no animal species have been identified i.e. file is 'Corrupt' or
                    no movement was detected.

      '60s indicator' - This column will contain either: 

                      - 'Yes' to indicate that the indicator appeared within the video.

                      - 'No' to indicate that the indicator did not appear in the video.
