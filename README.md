# Animal_classification_system
Copyrighted by Lewis Taylor

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
      
      User Interface: 
      
      ![image](https://user-images.githubusercontent.com/65728188/189195460-1dc0fd46-835e-4e33-b82d-8e1d8d35d592.png)

      
      <img width="553" alt="image" src="https://user-images.githubusercontent.com/65728188/189193995-3da971f5-2e2b-4140-be6d-e62eee56ca58.png">
      
      Beginging of processing:
      
      <img width="785" alt="image" src="https://user-images.githubusercontent.com/65728188/189194264-7997a298-8c64-40d9-98a8-de796a2e4774.png">
      
      Movement detection visual display: 
      
      <img width="749" alt="image" src="https://user-images.githubusercontent.com/65728188/189194592-6e6f3d12-9351-49ba-8280-60ef8f610cc5.png">
      
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
