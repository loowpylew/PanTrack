import os

DIR = 'D:\CT_2020'
i = 0

for root, dirs, files in os.walk(DIR): 
        for file in files:
            if file.endswith('.AVI') or file.endswith('.MP4'): 
                i += 1

print(i)
                