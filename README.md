# Animal-classification-system: PanTrack (Raw code version)

Copyrighted by Liam Taylor and Lewis Taylor

In order to run this software, upon running the excel_automation.py file you will be requested by the terminal to install various modules which are used by the software to call specific functions (i.e. ‘pip install opencv-python’ - a module used to read the txt within an image/video file).

Packages to install: 

pip install xlsxwriter

pip install opencv-python

pip install pandas 

pip install colorama

pip install pytesseract

pip install pynput

You can search the pip command for a specific module requested by the terminal using the following link: https://pypi.org/.

How to install pip for windows (used to install python modules):
https://phoenixnap.com/kb/install-pip-windows

You will need to open the file up with python. This will require you to download the python compiler. You can download the latest version from: https://www.python.org/downloads/

You will also be required to install the tesseract python distribution to perform Optimal Character Recognition (early machine-learning technique, used to decipher text within images).

Tesseract download page: https://tesseract-ocr.github.io/tessdoc/Downloads.html

Direct link to both 32 and 64 bit .exe file extensions for tesseract: https://github.com/UB-Mannheim/tesseract/wiki

Next, download the third party .exe file extensions for Windows. By default, when installed, the API's associated files can be found in program files within your PC's file system. To install the tesseract python distribution, type the following in the terminal: 
- pip install pytesseract

Optimal Character Recognition has been used within this script to identify the watermarked dates upon creation of a video as result of the camera being triggered by sudden movements.

The time span of each video is around 1 minute.

This software:
-	processes the file directory where an individual video is housed.

-	Processes the file name of the video.

-	Processes the date/time watermark in the video, and temperature watermark in the video (if present).

-	Identifies whether the videos are corrupt. 

-	Identifies movement within the video, within a manually adjustable range (the sensitivity is currently set at ….. – although any   sensitivity range between….. minimum and ….. maximum is suggested).

-	 All information is automatically loaded within an Excel spreadsheet which can then be further analysed by users using a programming language such as a ‘R’, ‘SPSS’, ‘python’, or any other software used for statistical analysis. 

Where a video is identified as corrupt, its corresponding row/cell will feature the word ‘Corrupt’ under the ‘Common’ column. 

Where no movement is detected in a video, its corresponding row/cell will feature the word ‘None’ under the ‘Common’ column, and the number ‘0’ under the ‘QUANTITY’ column.

-	All Excel output will automatically autofit columns, and freeze the first row (containing the variable names) for easier data visualisation. 
*The user of the software is only required to watch videos not labelled ‘None’ or ‘Corrupt’ under the ‘Common’ column.

Beginning of setup:

![image](https://user-images.githubusercontent.com/65728188/231834539-0d1a4afd-2ef0-4066-a0f0-3d28381c0dad.png)

Entering file directory to where cameras are housed:
 
![image](https://user-images.githubusercontent.com/65728188/231835009-f9ac69ae-2600-4536-92b8-edb678c00270.png)

Year specifier - Speeds up ability to process video watermark dates:

![image](https://user-images.githubusercontent.com/65728188/231835248-46900dde-a47f-422c-9124-4ca08dc39885.png)

Specifying filename (.xlsx) in which we want watermark/movement data to be populated: 
(File with existing name and file extension will be overwritten)

![image](https://user-images.githubusercontent.com/65728188/231835602-f6d7ccc7-fc2f-466a-acac-adf9db24f591.png)

Sensitivity specifier for movement detection: 

![image](https://user-images.githubusercontent.com/65728188/231836002-1437ef44-622c-487b-8048-9b62b5746022.png)

Movement detetcion viewer selector optionality:

![image](https://user-images.githubusercontent.com/65728188/231836266-35f9db81-533c-41f8-bc15-55fcf41fb06d.png)

Cameras being processed: 

![image](https://user-images.githubusercontent.com/65728188/189197192-0d005c91-2d51-4003-879e-195c9fab3a27.png)

Movement detection visual display: 

![image](https://user-images.githubusercontent.com/65728188/189197318-4e5ea4db-d04c-47b0-bff2-4d4ff84315a1.png)

The following columns will be manipulated:

'' - This will contain the index of each row, this is an automatic response by the ExcelWriter() function which is used to write all data captured to the specified excel spreadsheet.

'ROW' - This column will remain empty (outside the scope of this software's purpose).

'TREETAG' - This column will contain the camera name used to record the video within the corresponding row.

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
     - 'None' to indicate no movement was detected within the video recording. 

     - 'Corrupt' to indicate the video was not playable. 

     - '' (cell left empty) to indicate that the video has potential for animals to be present.

'SCIENTIFIC' - This column will remain empty (outside the scope of this software's purpose).

'QUANTITY' - This column will contain either:
       - '0.0' to indicate no animal species have been identified i.e. file is 'Corrupt' or
          no movement was detected.
