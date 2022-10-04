#! /usr/bin/env python
"""
Change OPERA 12 filename extensions from .tmp to valid ones
(as they were displayed in OPERA 8)
Target Users: Me
Target System: Windows
Year: 2014
Interface: None(batch job)
Functional Requirements:
        Recognize .flv, .exe, .jpg, .jpeg, .bmp, .gif,
        .doc, .txt files and change filename's extensions to them
        accordingly.
        As far as I can judge this info is in the first line of files.
Testing: none
Test values: none
"""
__version__ = 0.0
__maintainer__ = "me"
__status__ = "Prototype"

import os
import shutil
import os.path as p
import sys
import re
import errno

# To start with, I need to obtain the location of files to covert.
# If nothing is typed, I will assume default location:
# %USERPROFILE%\AppData\Local\opera\opera\cache
# C:\Users\Minchenkov_S\AppData\Local\Opera\Opera\cache
opera_cache_path ='C:/Users/Minchenkov_S/AppData/Local/Opera/Opera/cache'

# And I need to obtain the location where to saved converted files.
# If nothing is typed, I will assume default location:
# C:/Users/Minchenkov_S/Documents/Downloads
new_file_path ='C:/Users/Minchenkov_S/Documents/Downloads' 

# modules to be used later
def FileRename(destname,filename,filetype,n):
    try:
     inputname = destname+'/'+filename.split('_')[0]+'.tmp' 
#     if n >= 3:
     if n >= 1:
      raise PermissionError
     if n!=0:
       outputname= destname+'/'+filename+'_'+str(n)+'.'+filetype
     else:
       outputname= destname+'/'+filename+'.'+filetype
     n+=1
     os.rename(inputname,outputname)
    except FileExistsError:
      FileRename(destname,filename,filetype,n)
      return
    except FileNotFoundError:
      print('input file does not exist any more')
      return
    except PermissionError:
#       print('too much attempts to save')
      try:
        os.remove(inputname)
      except FileNotFoundError:
        pass
      return
    return      

# Prompt the user to input the paths.
opera_cache = input('Enter the path to input library: ')
if opera_cache == "":
  opera_cache=opera_cache_path
opera_save_dir = input('Enter the path to target library: ')
if opera_save_dir == "":
  opera_save_dir=new_file_path

# create a list of possible file extentions to check.  
extention=['png', 'tmp', 'jfif', 'exif', 'jpg', 'jpeg', 'gif', 'mp4', 'flv',
           'avi', 'pdf', 'mpg', 'ico', 'swf']

for t in os.walk(opera_cache):
  for i in range(len(t[2])):
   if t[2][i].split('.')[1].lower()=='tmp': 
    filepath = t[0]+'/'+t[2][i]
    filename =''
    testfile = open(filepath,'rb')
    firstrow=testfile.readline().strip()
    for e in extention:
     if re.search(e.encode('ASCII'),firstrow[0:70],re.DOTALL+re.IGNORECASE):
       shutil.copy2(filepath, opera_save_dir)
       filetype=e
       if e=='exif' or e=='jfif':
         filetype='jpg'
       filename= t[2][i].split('.')
       filename= filename[0]
#       newfilepath1=t[0]+'/'+filename+'.'+filetype 
       print(filename+'.'+filetype)
    testfile.close()
    if filename != "":
#     os.rename(filepath, newfilepath1)
      k=0
      FileRename(opera_save_dir,filename,filetype,k)


#import glob        
##os.chdir(opera_cache+'/g_002E')
##print(os.getcwd())
##
###for item in glob.glob(opera_cache+'/g_002E'):
##for item in glob.glob('*'): 
##   if p.isfile(item): print(item, ' is a file')
##   elif p.isdir(item): print(item, ' is a directory')
##   else: print(item, ' is of unknown type')
##   print('qq ', item)

# rename(item, file)

#sys.exit()
