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
	if platform.system() == 'Windows':
		print("Mapping network drive in Windows.")
		commandString = "pushd " + mapNetworkDrive
		print(commandString)
		p = subprocess.Popen(commandString,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
		output, err = p.communicate()
		if output.decode('ascii') == '':
			print("Mapping network drive was unsuccessful")
		else:
			print("Mapping network drive was successful")

	elif platform.system() == 'Linux':
		print("Mapping network drive in Linux.")
	else:
		print("The script is being tried to run on a platform outside the scope of the covergae of this tool. Please note that mapping the network drive would not be possible")

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Generic Automated System test tool Script to run test scripts from a remote location. Please note that if the map network drive option is not provided the script looks for the files/directory provided in the argument under its root directory structure.")
	parser.add_argument('-t','--testScriptFileName', dest='testScriptFileName', help='absolute path for the test script that needs to be run in slave system.')
	parser.add_argument('-d','--testScriptDirectory', dest='testScriptDirectory', help='absolute path for the directory containing the test scripts.')
	parser.add_argument('-m','--mapNetworkDrive', dest='mapNetworkDrive', help='This option is used to map a network drive on to the framework.')

	args = parser.parse_args()
	testScriptFileName = args.testScriptFileName
	testScriptDirectory = args.testScriptDirectory
	mapNetworkDrive = args.mapNetworkDrive

	if mapNetworkDrive is not None:
		mappingNetworkDrive(mapNetworkDrive)
