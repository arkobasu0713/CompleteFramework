import os
import database as db
import mysql.connector as MConn
import subprocess
import random
import argparse
import sys
import os
import time
import platform
from mysql.connector import errorcode

def processNewEntrySoftPackage(softPackageName,softwarePackageLocation,conn):
	generateSoftPackID = random.randint(0,9999)
	currDate = time.strftime("%Y-%m-%d")
	loadMethod = 'GUI'
	add_software_pack_query = ("INSERT INTO SOFTWARE_PACKAGE_LOAD VALUES (%(softPackID)s,%(softPackageName)s,%(currDate)s,%(loadMethod)s,%(softwarePackageLocation)s,%(depMod)s)")
	data = {'softPackID': generateSoftPackID, 'softPackageName': softPackageName, 'currDate': currDate, 'loadMethod': loadMethod, 'softwarePackageLocation': softwarePackageLocation, 'depMod': 0,}
	try:
		conn.cursor.execute(add_software_pack_query,data)
		conn.cnx.commit()
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		return e
	else:
		return 'Success'

def deleteCommand(conn,commandIDs,softPackageID):
	deleteCommand_query = ("DELETE FROM SOFTWARE_COMMANDS WHERE COMMAND_ID = %s AND SOFTWARE_PACKAGE_ID = %s")
	executeData = []
	print(commandIDs)
	print(softPackageID)
	try:
		for eachCommandID in commandIDs:
			conn.cursor.execute(deleteCommand_query,[eachCommandID,softPackageID,])
			conn.cnx.commit()
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		return e
	else:
		return 'Success'

def processNewEntryCommand(commandName,conn,hasMand,hasOpt):
	addCommandQuery = ("INSERT INTO SOFTWARE_COMMANDS VALUES (%(softPackID)s,%(commandID)s,%(commandName)s,%(hasMand)s,%(hasOpt)s)")
	data = {'softPackID':conn.softwarePackageID,'commandID':None,'commandName': commandName,'hasMand':hasMand,'hasOpt':hasOpt,}
	try:
		conn.cursor.execute(addCommandQuery,data)
		conn.cnx.commit()
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		return e
	else:
		return 'Success'


def RunScript(commandString):

	"""Runs a command string.
	Returns the object of Popen once the command is run."""

	p = subprocess.Popen(commandString,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	return p

def createOutputFile(fileName,outputLocation):
	outputFileLocation = outputLocation
	justFileName = (os.path.basename(fileName)).split('.txt')[0]
	
	outputLogFileName = justFileName + ".log"
	outputLogFileLoc = os.path.join(outputFileLocation, outputLogFileName)
	file =open(outputLogFileLoc,'w')
	return file
def createScript(commandName,outputLocation):

	fileName = commandName + ".txt"
	filePath = os.path.join(outputLocation,fileName)
	file = open(filePath, 'w')
	print("File " + filePath +" for command, " + commandName +" created")
	return file, filePath

def createOutputLogDirectory(logFilePath):

	"""This method creates the Output Log Directory.
	Returns the path to the output log directory."""

	if logFilePath == '' or logFilePath is None:
		print("No log file path provided in the argument. Hence creating in the default directory location.")
		defLogLocation = os.path.join(os.path.dirname(__file__),'..','DBExtract')
		if os.path.exists(defLogLocation):
			print("Default Log Path already exists.")
			return defLogLocation
		else:
			os.mkdir(defLogLocation)
			return defLogLocation
	else:
		if not os.path.exists(logFilePath):
			os.mkdir(logFilePath)
			return logFilePath
		elif os.path.exists(logFilePath):
			print("Argument Location provided for generating log files already exists.")
			return logFilePath

def establishConnection():
	print("Trying to establish connection with the following config:")
	print(db.mysql)
	try:
		cnx = MConn.connect(**db.mysql)
		cursor = cnx.cursor()
	except MConn.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with credentials in the database py file")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Specified database doesn't exist")
		else:
			print(err)
	else:
		print("Connection Successful.")
	return cnx, cursor

class enterDBSpace():

	def __init__(self):
		self.cnx, self.cursor = establishConnection()
		self.dictOfPackages = {}
		self.dictOfCommands = {}
		self.dictOfCommandArguments = {}
		self.dictOfArguments = {}
		self.dictOfArgVal = {}
		self.softwarePackage = '' 
		self.softwarePackageID = 0
		self.fileNames = []
		self.dictOfFileNames = {}
		self.dictOfArgumentTypes = {}
		self.dictOfArgVal2 = {}

	def reEstablishConnection(self):
		self.cnx.close()
		self.cursor.close()
		self.cnx, self.cursor = establishConnection()
		

	def fetchSoftPackage(self):
		print("inconnect")
		self.dictOfPackages.clear()
		print(self.dictOfPackages)
		self.cursor.execute("SELECT SOFTWARE_PACKAGE_ID,SOFTWARE_PACKAGE_NAME FROM SOFTWARE_PACKAGE_LOAD")
		data = self.cursor.fetchall()
		for package_id, package in data:
			self.dictOfPackages[package_id] = package

	def retreiveCommandsUnderSoftwarePackage(self,ID):
		self.dictOfCommands.clear()
		self.cursor.execute("select COM.COMMAND_ID, COM.COMMAND_DESC FROM SOFTWARE_PACKAGE_LOAD SOFT, SOFTWARE_COMMANDS COM WHERE COM.SOFTWARE_PACKAGE_ID = SOFT.SOFTWARE_PACKAGE_ID AND SOFT.SOFTWARE_PACKAGE_ID = %s",(ID,))
		data = self.cursor.fetchall()
		for commandID, command in data:
			self.dictOfCommands[commandID] = command


	def fetchArgumentsForSelectCommands(self, comSelect):
		self.comSelect = comSelect
		self.dictOfCommandArguments = {}
		self.dictOfArguments = {}
		for eachCommandID in self.comSelect:

			self.cursor.execute("SELECT ARG.ARGUMENT_ID, ARG.ARGUMENT FROM ARGUMENTS ARG, SOFTWARE_COMMANDS COM WHERE COM.COMMAND_ID = ARG.COMMAND_ID AND COM.SOFTWARE_PACKAGE_ID = ARG.SOFTWARE_PACKAGE_ID AND COM.COMMAND_ID = %s",(eachCommandID,))

			data = self.cursor.fetchall()
			argID = [x[0] for x in data]
			arg = [x[1] for x in data]
			
			self.dictOfCommandArguments[eachCommandID] = argID

			for i in range(len(argID)):
				self.dictOfArguments[argID[i]] = arg[i]

			


	def retreiveValuesForArguments(self):
		self.dictOfArgVal = {}
		self.dictOfArgVal2 = {}
		for argSet in self.dictOfCommandArguments:
			for eachArg in self.dictOfCommandArguments[argSet]:
				self.dictOfArgumentTypes = {}
				self.cursor.execute("select ARGUMENT_VAL_TYPE, DEFAULT_VALUE from ARGUMENT_VALUES WHERE ARGUMENT_ID = %s",(eachArg,))
				data = self.cursor.fetchall()
				listOfValues=[]
				for eachValType, defVal in data:
					if eachValType in ['ABP','STR']:
						listOfValues.append(defVal)
					self.dictOfArgumentTypes[eachValType] = defVal
				self.dictOfArgVal[eachArg] = listOfValues
				self.dictOfArgVal2[eachArg] = self.dictOfArgumentTypes

	def createScripts(self,logFilePath,comSelect):
		self.outputLocation = createOutputLogDirectory(logFilePath)
		self.dictOfFileNames = {}
	
		for eachCommandID1 in comSelect:
			file1, filename = createScript(self.dictOfCommands[eachCommandID1],self.outputLocation)
			self.dictOfFileNames[eachCommandID1] = filename

#		print(self.dictOfFileNames)

		for eachCommandID2 in comSelect:
			writeFile = open(self.dictOfFileNames[eachCommandID2],'w')
			
			writeFile.write(str(self.softwarePackage) + " " + str(self.dictOfCommands[eachCommandID2]))
			writeFile.write('\n')
			for eachArg in self.dictOfCommandArguments[eachCommandID2]:
				writeFile.write(str(self.softwarePackage) + ' ' + str(self.dictOfCommands[eachCommandID2]) + ' ' + str(self.dictOfArguments[eachArg]))
				writeFile.write('\n')
				for eachArgVal in self.dictOfArgVal[eachArg]:
					writeFile.write(str(self.softwarePackage) + ' ' + str(self.dictOfCommands[eachCommandID2]) + ' ' + str(self.dictOfArguments[eachArg]) + ' ' + str(eachArgVal))
					writeFile.write('\n')

	def runScripts(self):
		dictOfStatus = {}
		print(self.dictOfFileNames)

#	"""Run each of the scripts found in the temp script and writes them in the output file object."""
		for eachFileID in self.dictOfFileNames:
			writeFile = createOutputFile(self.dictOfFileNames[eachFileID],self.outputLocation)
			readFile = open(self.dictOfFileNames[eachFileID],'r')
			numOfScripts = 0
			fail = 0
			success = 0
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
			dictOfStatus[self.dictOfFileNames[eachFileID]] = list([success,fail,numOfScripts])
		
		return dictOfStatus


	def connectionClose(self):		
		self.cursor.close()
		self.cnx.close()
	

