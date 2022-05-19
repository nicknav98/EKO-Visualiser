# Fetches files from specific folder
# Built with Python 3.8
# Author: Nicholas Navarro
# First Revision: 19.5.22

import glob
import os
import shutil

new_src = './testData'
list_of_files = glob.glob('./testData/Backup/*.CSV') # gets lists of files form specific directory
latest_file = max(list_of_files, key=os.path.getctime) # finds latest file
print("Copying latest CSV file" + latest_file + "\n") # prints message
shutil.copy2(latest_file, new_src) # copies to new directory

