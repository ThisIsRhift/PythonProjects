# Created by: Jared Jensen
# Created date: 04/11/2018
# cd c:\Python27
# python C:\Users\jared.jensen\Documents\exploreFileTree.py
import os
import zipfile
import datetime

# Variables -edit these to match file you are searching for and starting directory
fileName = "dly_sys_ttl.csv"  #Name of missing file
baseDirectorySourceFile = "C:\Users\jared.jensen\Documents\Dirs.txt" #Source file of directories to search 
outputDir = "C:\Users\jared.jensen\Desktop" #Output file location

# Program variables
currentDate = datetime.datetime.now().strftime ("%Y%m%d")
yesterdayDate = datetime.datetime.now() - datetime.timedelta(days=1)
todaysFile = yesterdayDate.strftime("%Y%m%d") + ".zip"
fileLocations = []
startingDir = [] 
locationsMissingFiles = []
outFileName = outputDir + "\Missing_data_"+currentDate+".txt"

# Copy contents of baseDirectorySourceFile into an array and remove line endings - \n
with open(baseDirectorySourceFile,"r") as ins:
	for line in ins:
		startingDir.append(line.rstrip('\n'))

print("Directories loaded")
print("Searching " + str(len(startingDir)) +" locations for " +todaysFile)

# Find all files with the name stored in todaysFile
while len(startingDir) > 0:
	searchDir = startingDir.pop()
	for root, dirs, files in os.walk(searchDir):
		for file in files:
			if file.endswith(todaysFile):
				fileLocations.append(os.path.join(root, file))

print(str(len(fileLocations)) + " files found")

# Checks each zip file in fileLocations for missing file, fileName
while len(fileLocations) > 0:
	fileDir = fileLocations.pop()
	zf = zipfile.ZipFile(fileDir)
	try:
		zf.getinfo(fileName)
	except KeyError:
		locationsMissingFiles.append(fileDir)
	else:
		print(fileDir)

# if locationsMissingFiles is empty write No missing files to outFileName
if len(locationsMissingFiles) == 0:
	file = open(outFileName,'a')
	file.write("No missing files")
	file.close()
	
# Writes location of missing files to outFileName
while len(locationsMissingFiles) > 0:
	path = locationsMissingFiles.pop()
	file = open(outFileName,'a')
	file.write("Missing "+fileName+ " in " +path+"\n")
	file.close()
	print("Missing "+fileName+ " in " +path)