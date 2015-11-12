#!/usr/local/bin python3
#Author: Arko Basu
#Date  : 11122015
#Copyright: HGST Inc.
#Description: Generic Automated Tool
import argparse
import sys
import os
import time
import platform
import subprocess
import shutil
import glob

def RunScript(commandString):

	"""Runs a command string.
	Returns the object of Popen once the command is run."""

	p = subprocess.Popen(commandString,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	return p

def mappingNetworkDrive(mapNetworkDrive):
	print("Current OS the script is running on: " + str(platform.system()))
	if platform.system() == 'Windows':
		print("Mapping network drive in Windows.")
		
		#formatting the command string for mapping the network drive
		commandString = "net use q: " + mapNetworkDrive

		username = input("Enter username(optional): ")
		password = input("Enter password(optional): ")

		if username and password != '':
			commandString = commandString + "/user:" + username + " " + password
		else:
			print("Error in username password. Going ahaed with deafult values") #needs to be worked upon
		
		print("Cmd String: " + commandString)
		p = subprocess.Popen(commandString,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
		output, err = p.communicate()
		if output.decode('ascii') == '':
			print("Mapping network drive was unsuccessful")
			print(err.decode('ascii'))
		else:
			print("Mapping network drive was successful")
		return "q:"

	elif platform.system() == 'Linux':
		print("Mapping network drive in Linux.")
		
		
		#formatting the command string for mapping the network drive
		commandString = "mount -t cifs -w " + mapNetworkDrive
		yOrN = (input("Do you wish to create the mount for the network drive somewhere specific(y). Otherwise the mount directory would be created in within the current root directory of the setup script: ")).upper()
		if yOrN == 'Y':
			mountLocation = input("Please enter the absolute path of the mount location: ")
			print(mountLocation)
		else:
			print("Creating mount location within directory structure.")
			mountLocation = os.path.join(os.getcwd(),("mountLocation"+str(time.strftime("%Y-%m-%d"))))
			print("Mount location being used: " + mountLocation)
			if not os.path.exists(mountLocation):
				print("Path doesn't exist. Creating Mount location")
				try:
					os.mkdir(mountLocation)
				except OSError as exc:
					if exc.errno == errno.EEXIST and os.path.isdir(mountLocation):
						pass
					else: raise

		username = input("Enter username(optional): ")
		password = input("Enter password(optional): ")

		commandString = commandString + " " + mountLocation

		if username and password != '':
			commandString = commandString + " -o username=" + username + ",password=" + password
		else:
			print("Error in username password. Going ahead with default values") #needs to be worked upon
			commandString = commandString + " -o username=disty,password=sitlab"
		
		print("Cmd String: " + commandString)
		p = subprocess.Popen(commandString,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
		output, err = p.communicate()
		if output.decode('ascii') == '' and err.decode('ascii') == '':
			print("Mapping network drive was successful")
		else:
			print("Mapping network drive was unsuccessful")
			print(err.decode('ascii'))
		return mountLocation
	else:
		print("The script is being tried to run on a platform outside the scope of the covergae of this tool. Please note that mapping the network drive would not be possible")
		return ''

def createOutputFile(fileName,logDest):
	outputFileLocation = logDest
	justFileName = (os.path.basename(fileName)).split('.txt')[0]
	
	outputLogFileName = justFileName + ".log"
	outputLogFileLoc = os.path.join(outputFileLocation, outputLogFileName)
	file =open(outputLogFileLoc,'w')
	return file

def runScript(scriptName,logDest):
	writeFile = createOutputFile(scriptName,logDest)
	readFile = open(scriptName,'r')
	numOfScripts = 0
	fail = 0
	success = 0
	print("Running Script: " + scriptName)
	for eachLine in readFile:
		writeFile.write("=====================================================================\n")
		writeFile.write("Running: " + eachLine)
		writeFile.write('\n')
		p = RunScript(eachLine)
		output, err = p.communicate()
		if output.decode('ascii') == '':
			writeFile.write(err.decode('ascii'))
			fail = fail + 1
		else:
			writeFile.write(output.decode('ascii'))
			success = success + 1
		writeFile.write("\n")
		numOfScripts = numOfScripts + 1
		writeFile.write("---------------------------------------------------------------------\n")
		if output.decode('ascii') == '':
			writeFile.write("Command execution Status: FAILED\n")
			writeFile.write("Class of ERROR code: " + str(p.returncode) + '\n')
		else:
			writeFile.write("Command execution Status: SUCCESS\n")
		writeFile.write("=====================================================================\n")
	print("\tRun Complete.")
	print("\tTotal number of commands executed from the scripts: " + str(numOfScripts))
	print("\tNumber of execution failures: " + str(fail))
	print("\tNumber of execution success: " + str(success))


def createLogDest(logDest):
	
	if not os.path.exists(logDest):
		print("Path doesn't exist. Creating Mount location")
		try:
			os.mkdir(logDest)
		except OSError as exc1:
			if exc1.errno == errno.EEXIST and os.path.isdir(mountLocation):
				pass
			else: raise
	return logDest

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Generic Automated System test tool Script to run test scripts from a remote location. Please note that if the map network drive option is not provided the script looks for the files/directory provided in the argument under its root directory structure.")
	parser.add_argument('-t','--testScriptFileName', dest='testScriptFileName', help='absolute path for the test script that needs to be run in slave system.')
	parser.add_argument('-d','--testScriptDirectory', dest='testScriptDirectory', help='absolute path for the directory containing the test scripts. Please note that this needs to be run with')
	parser.add_argument('-m','--mapNetworkDrive', dest='mapNetworkDrive', help='This option is used to map a network drive for the extraction of the scripts from a remote server location for the framework. You could add -d/--testScriptDirectory option along with this to specify the folder name inside the network drive.')
	parser.add_argument('-u','--unMapNetworkDrive',dest='unMapNetworkDrive',help='run this option alone after using the test script to unmap the network drive')

	args = parser.parse_args()
	testScriptFileName = args.testScriptFileName
	testScriptDirectory = args.testScriptDirectory
	mapNetworkDrive = args.mapNetworkDrive
	unMap = args.unMapNetworkDrive

	dictOfFileNames = {}
	dictOfSpecificFileNames = {}
	mapDriveAt = ''

	if mapNetworkDrive is not None:
		mapDriveAt = mappingNetworkDrive(mapNetworkDrive)
		i = 1
		for root, dirs, f in os.walk(mapDriveAt):
			for files in f:
				if files.endswith(".txt"):
					dictOfFileNames[i] = os.path.join(root,files)
					i = i + 1

	if testScriptFileName is not None:
		j=1
		for eachValue in dictOfFileNames:
			if testScriptFileName in dictOfFileNames[eachValue]:
				dictOfSpecificFileNames[j] = dictOfFileNames[eachValue]
				j=j+1

	while True:
		
		try:
			print("The following script files were found in the remote network drive: ")
			print(dictOfFileNames)
			run = (input("Enter the numbers from the above list to run specific scripts separated with a semicolon(;) Or enter 0 (Zero) to execute all scripts: ")).split(';')
			run = [int(i) for i in run]
			logDest = ''
			logDest = input(("Enter the location that you want to create the log files at. Hit enter and keep blank for the system to create a datetime stamped folder in the root directory of the setup script: ")).upper()
			if logDest == '':
				logDest = os.path.join(os.getcwd(),("LogDump"+str(time.strftime("%Y-%m-%d-%m-%s"))))
			createLogDest(logDest)
			if len(run) == 1 and run[0] == 0:
				for eachFile in dictOfFileNames:
					runScript(dictOfFileNames[eachFile],logDest)
			else:
				for serialScriptNum in run:
					runScript(dictOfFileNames[serialScriptNum],logDest)
			transfer = (input("Do you wish to copy the folder generated with logs to the remote directory?(y): ")).upper()
			if transfer == 'Y':
				for filename in os.listdir(logDest):
					fullFileName = os.path.join(logDest,filename)
					if (os.path.isfile(fullFileName)):
						try:
							shutil.copy(fullFileName,mapDriveAt)
						except OSError as exc:
							print(exc.strerror)
						
						else:
							print("Copy of " + fullFileName + " to remote drive " + mapDriveAt + " successful.")
			
			cont = (input("Do you wish to continue testing other scripts?(y): ")).upper()
			if cont != 'Y':
				break

		except OSError as exc:
			print(exc.errno)


			
