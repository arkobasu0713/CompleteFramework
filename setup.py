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

def mappingNetworkDrive(mapNetworkDrive):
	print("Checking OS reqirements:")
	print("Current OS the script is running on: " + str(platform.system()))
	print(mapNetworkDrive)
	if platform.system() == 'Windows':
		print("Mapping network drive in Windows.")
		
		#formatting the command string for mapping the network drive
		commandString = "net use q: " + mapNetworkDrive

		username = input("Enter username(optional): ")
		password = input("Enter password(optional): ")
		print(username)
		print(password)

		if username and password != '':
			commandString = commandString + "/user:" + username + " " + password
		else:
			print("Error in username password.") #needs to be worked upon
		
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

		print(username)
		print(password)

		commandString = commandString + " " + mountLocation

		if username and password != '':
			commandString = commandString + " -o username=" + username + ",password=" + password
		else:
			print("Error in username password. Going with default values") #needs to be worked upon
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
		sys.exit(0)

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Generic Automated System test tool Script to run test scripts from a remote location. Please note that if the map network drive option is not provided the script looks for the files/directory provided in the argument under its root directory structure.")
	parser.add_argument('-t','--testScriptFileName', dest='testScriptFileName', help='absolute path for the test script that needs to be run in slave system.')
	parser.add_argument('-d','--testScriptDirectory', dest='testScriptDirectory', help='absolute path for the directory containing the test scripts.')
	parser.add_argument('-m','--mapNetworkDrive', dest='mapNetworkDrive', help='This option is used to map a network drive for the extraction of the scripts from a remote server location for the framework. You could add -d/--testScriptDirectory option along with this to specify the folder name inside the network drive.')
	parser.add_argument('-u','--unMapNetworkDrive',dest='unMapNetworkDrive',help='run this option alone after using the test script to unmap the network drive')

	args = parser.parse_args()
	testScriptFileName = args.testScriptFileName
	testScriptDirectory = args.testScriptDirectory
	mapNetworkDrive = args.mapNetworkDrive
	unMap = args.unMapNetworkDrive

	while True:
		try:
			if mapNetworkDrive is not None:
				mapDriveAt = mappingNetworkDrive(mapNetworkDrive)
		except OSError as exc:
			print(exc.errno)
			break
			
