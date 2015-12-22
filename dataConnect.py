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
from dynamicUtilsUI import * 

def deleteTestSuit(*args):
	print("In procedure to delete list of selected test suits with ID")
	testSuitSelection = tuple(args[0])
	conn = args[1]
	print(tuple(testSuitSelection))
	if len(testSuitSelection) > 1:
		query = "DELETE FROM SOFTWARE_COMMAND_TEST_SUIT WHERE TEST_SUIT_ID IN {0}".format(testSuitSelection)
	else:
		query = "DELETE FROM SOFTWARE_COMMAND_TEST_SUIT WHERE TEST_SUIT_ID = {0}".format(testSuitSelection[0])
		
	print(query)
	try:
		conn.cursor.execute(query)
		conn.cnx.commit()
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		popupFailure = createP1('Failure','Database transaction of deleting test suits',"Unsuccessful transaction on table SOFTWARE_COMMAND_TEST_SUIT",e)
		popupFailure.open()
	else:
		popupSuccess = createP1('Success','Database transaction of deleting test suits',"Successful transaction on table SOFTWARE_COMMAND_TEST_SUIT")
		popupSuccess.open()
		#boxForValueDisplay.add_widget()
		print('Success')
	
def saveTestSuit(*args):
	print("In procedure for saving test suits")
	conn = args[0]
	softwarePackageID = conn.softwarePackageID
	command = args[1]
	argumentIDs = args[2]
	testSuitName = args[3].text
	
	print("SoftwarePackageID: " + str(softwarePackageID))
	print("CommandID: " + str(command))
	print("ArgumentIDs: "+ str(argumentIDs))
	print("TestSuitName: " + testSuitName)
	testSuitID = random.randint(0,9999)
	print("TestSuitID: " + str(testSuitID))
	
	try:
		for eachArgumentID in argumentIDs:
			query = "INSERT INTO SOFTWARE_COMMAND_TEST_SUIT VALUES ({0},{1},{4},'{2}',{3})".format(softwarePackageID,command,testSuitName,eachArgumentID,testSuitID)
			print(query)
			conn.cursor.execute(query)
			conn.cnx.commit()
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		popupFailure = createP1('Failure','Database transaction of saving Test Suit',"Unsuccessful transaction on table SOFTWARE_COMMAND_TEST_SUIT",e)
		popupFailure.open()
	else:
		popupSuccess = createP1('Success','Database transaction of saving Test Suit',"Successful transaction on table SOFTWARE_COMMAND_TEST_SUIT")
		popupSuccess.open()
		print('Success')
		
def saveArgumentValue(*args):
	print("In procedure to save argument value")
	selectionArgumentID = args[1][0]
	conn = args[2]
	boxForValueDisplay = args[3]
	argValueType, argumentDefaultParameter, argumentDefaultValue= extractData(args[0])
	print("Value Type: " + argValueType)
	if argumentDefaultParameter == '':
		argumentDefaultParameter = ''
	print("Default parameter: " + str(argumentDefaultParameter))
	print("Default value: " + argumentDefaultValue)
	query = "INSERT INTO ARGUMENT_VALUES VALUES({0},'{1}','{2}','{3}')".format(selectionArgumentID,argValueType,argumentDefaultValue,argumentDefaultParameter)
	print(query)
	try:
		conn.cursor.execute(query)
		conn.cnx.commit()
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		popupFailure = createP1('Failure','Database transaction of saving Argument Values',"Unsuccessful transaction on table ARGUMENT_VALUES",e)
		popupFailure.open()
	else:
		popupSuccess = createP1('Success','Database transaction of saving Argument Values',"Successful transaction on table ARGUMENT_VALUES")
		popupSuccess.open()
		del args[1][:]
		#boxForValueDisplay.add_widget()
		print('Success')
		
	
def deleteArgumentValues(*args):
	print("In procedure to delete argument values")
	print("Argument ID: " + str(args[0]))
	print("Argument Values to be deleted: "+str(args[1]))
	conn = args[2]
	try:
		for eachValueSet in args[1]:
			query = "DELETE FROM ARGUMENT_VALUES WHERE ARGUMENT_ID = {0} AND ARGUMENT_VAL_TYPE = '{1}' and DEFAULT_VALUE = '{2}'".format(args[0],eachValueSet[0],eachValueSet[1])
			print(query)
			conn.cursor.execute(query)
			conn.cnx.commit()
			
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		#return e
		popupFailure = createP1('Failure','Deletion of Selected Argument Values',"Unsuccessful transaction on table ARGUMENT_VALUES",e)
		popupFailure.open()
	else:
		#return 'Success'
		popupSuccess = createP1('Success','Deletion of selected arguments values',"Successful transaction on table ARGUMENT_VALUES")
		popupSuccess.open()
		print('Success')
	

def deleteArgDetails(listOfArgIDs,conn):
	listOfArg = [int(i) for i in listOfArgIDs]
	tupOfArg = (tuple(listOfArg))
	print(listOfArg)
	print(tupOfArg)
	if len(tupOfArg) > 1:
		deleteValuesData = "DELETE FROM ARGUMENT_VALUES WHERE ARGUMENT_ID IN {0}".format(str(tupOfArg))
		deleteArgData = "DELETE FROM ARGUMENTS WHERE SOFTWARE_PACKAGE_ID = %s AND ARGUMENT_ID IN " + str(tupOfArg)
	elif len(tupOfArg) == 1 :
		deleteValuesData = "DELETE FROM ARGUMENT_VALUES WHERE ARGUMENT_ID = {0}".format(str(tupOfArg[0]))
		deleteArgData = "DELETE FROM ARGUMENTS WHERE SOFTWARE_PACKAGE_ID = %s AND ARGUMENT_ID = " +str(tupOfArg[0])
	print(deleteValuesData)
	print(deleteArgData)
	try:
		flag1 = 0
		flag2 = 0
		conn.cursor.execute(deleteValuesData)
		flag1=1
		conn.cnx.commit()
		conn.cursor.execute(deleteArgData,[conn.softwarePackageID,])
		flag2=1
		conn.cnx.commit()
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		#return e
		if flag1 != 1:
			popupFailure = createP1('Failure','Deletion of Argument Values',"Unsuccessful transaction on table ARGUMENT_VALUES",e)
		elif flag2 != 1:
			popupFailure = createP1('Failure','Deletion of Arguments',"Successful Transaction on ARGUMENT_VALUES but, Unsuccessful transaction on table ARGUMENTS",e)
		popupFailure.open()
		return 0
	else:
		#return 'Success'
		popupSuccess = createP1('Success','Deletion of Arguments and their Values',"Transaction for arguments and corresponding values were successful")
		popupSuccess.open()
		print('Success')
		return 1
	#print(deleteValuesData)
	#print(deleteArgData)
	
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
		
def processArgEntry(*args):
	print("Processing Argument Entry")
	commandID = int(args[1])
	arg = args[0]
	conn = args[2]
	txtInptImport = args[3].text
	commandIDImportsFrom = args[4].id
	softPackID = conn.softwarePackageID
	print(commandIDImportsFrom)
	query = ("INSERT INTO ARGUMENTS VALUES (%(softPackID)s,%(commandID)s,%(argument)s,%(argumentID)s,%(ImportFrom)s,%(importsTag)s)")
	if commandIDImportsFrom != "btnID":
		data = {'softPackID':softPackID, 'commandID': commandID, 'argument':arg.text, 'argumentID': None, 'ImportFrom': int(commandIDImportsFrom), 'importsTag': txtInptImport,}
		#print(data)
		argumentValuesQuery = ("INSERT INTO ARGUMENT_VALUES VALUES (%(argumentID)s,%(ARGUMENT_VAL_TYPE)s,%(DEFAULT_VALUE)s,%(DEFAULT_ARG_PARAMETER)s)")
		fetchQuery = ("SELECT ARGUMENT_ID FROM ARGUMENTS WHERE SOFTWARE_PACKAGE_ID = %s AND COMMAND_ID = %s AND ARGUMENT = %s")
	else:
		data = {'softPackID':softPackID, 'commandID': commandID, 'argument':arg.text, 'argumentID': None, 'ImportFrom': None, 'importsTag': None,}
	try:
		flag1 = 0
		flag2 = 0
		if arg.text != None and arg.text != "":
			#print(data)
			conn.cursor.execute(query,data)
			conn.cnx.commit()
			flag1 = 1
			if commandIDImportsFrom != 'btnID':
				conn.cursor.execute(fetchQuery,[softPackID,commandID,arg.text,])
				data1 = conn.cursor.fetchall()
				#print(data1)
				dataAct = data1[0][0]
				#print(dataAct)
				argumentValuesData = {'argumentID':dataAct,'ARGUMENT_VAL_TYPE':'IMP','DEFAULT_VALUE':None,'DEFAULT_ARG_PARAMETER':None,}
				#print(argumentValuesData)
				conn.cursor.execute(argumentValuesQuery,argumentValuesData)
				conn.cnx.commit()
				flag2 = 1
		else:
			print("No Update.")
	except MConn.Error as e:
		print("Error code: " + str(e.errno))
		print("Error Message: " + str(e.msg))
		print(str(e))
		if flag1 != 1:
			popupFailure = createP1('Failure','Database transaction of Arguments and Values',"Unsuccessful transaction on table ARGUMENTS",e)
		elif flag2 != 1:
			popupFailure = createP1('Failure','Database transaction of Arguments and Values',"Successful Transaction on ARGUMENTS but, Unsuccessful transaction on table ARGUMENT_VALUES",e)
		popupFailure.open()
	else:
		popupSuccess = createP1('Success','Database transaction of Arguments and Values',"Transaction for arguments and corresponding values were successful")
		popupSuccess.open()
		print('Success')
		
	
def deleteCommand(conn,commandIDs,softPackageID):
	deleteCommand_query = ("DELETE FROM SOFTWARE_COMMANDS WHERE COMMAND_ID = %s AND SOFTWARE_PACKAGE_ID = %s")
	argumentIDs = []
	
	for eachCommandID in commandIDs:
		for eachArgID in conn.dictOfCommandArguments[eachCommandID]:
			argumentIDs.append(eachArgID)
	
	listOfArg = [int(i) for i in argumentIDs]
	tupOfArg = (tuple(listOfArg))
	print(tupOfArg)
	
	
	if len(tupOfArg) > 1:
		deleteArgData = "DELETE FROM ARGUMENTS WHERE SOFTWARE_PACKAGE_ID = %s AND ARGUMENT_ID IN " + str(tupOfArg)
		deleteValuesData = "DELETE FROM ARGUMENT_VALUES WHERE ARGUMENT_ID IN" + str(tupOfArg)
		print(deleteArgData)
		print(deleteValuesData)
	elif len(tupOfArg) == 1 :
		deleteArgData = "DELETE FROM ARGUMENTS WHERE SOFTWARE_PACKAGE_ID = %s AND ARGUMENT_ID = " +str(tupOfArg[0])
		deleteValuesData = "DELETE FROM ARGUMENT_VALUES WHERE ARGUMENT_ID = " +str(tupOfArg[0])
		print(deleteArgData)
		print(deleteValuesData)
	else:
		deleteValuesData = ''
		deleteArgData = ''
	#print(commandIDs)
	#print(softPackageID)
	try:
		flag1 =0
		flag2 =0
		flag3 =0
		if deleteValuesData != '':
			conn.cursor.execute(deleteValuesData)
			flag1=1
			conn.cnx.commit()
		elif deleteValuesData == '':
			flag = 1
		if deleteArgData != '':
			conn.cursor.execute(deleteArgData,[conn.softwarePackageID,])
			flag2=1
			conn.cnx.commit()
		elif deleteArgData == '':
			flag2=1
		for eachCommandID in commandIDs:
			conn.cursor.execute(deleteCommand_query,[eachCommandID,softPackageID,])
		flag3=1
		conn.cnx.commit()
	except MConn.Error as e:
		print("Error Message: " + str(e.msg))
		print(str(e))
		return 0, flag1, flag2, flag3, e
	else:
		return 1, flag1, flag2, flag3, ''

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
	print("File " + filePath +" for command, " + commandName +" created")
	return filePath

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
		self.dictOfPackages.clear()
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
				
	def fetchTestSuits(self,*args):
		commandID = args[0]
		query1 = "select distinct TEST_SUIT_ID, TEST_SUIT_DESC FROM SOFTWARE_COMMAND_TEST_SUIT WHERE SOFTWARE_PACKAGE_ID = {0} AND COMMAND_ID = {1}".format(self.softwarePackageID,commandID)
		print(query1)
		try:
			self.cursor.execute(query1)
			data = self.cursor.fetchall()
			print(data)
		except MConn.Error as e:
			print("Error code: " + str(e.errno))
			print("Error Message: " + str(e.msg))
			print(str(e))
			return None
		else:
			return data
		
	def fetchArgumentsForTestSuit(self,*args):
		print("In procedure to retreive argument ids for selected test suit")
		testSuitID = args[0]
		command = args[1]
		print("TestSuitID: "+ str(testSuitID))
		query = "SELECT SCTS.ARGUMENT_ID, ARG.ARGUMENT FROM SOFTWARE_COMMAND_TEST_SUIT SCTS, ARGUMENTS ARG WHERE SCTS.SOFTWARE_PACKAGE_ID = {0} AND SCTS.TEST_SUIT_ID = {1} AND SCTS.COMMAND_ID = {2} AND SCTS.SOFTWARE_PACKAGE_ID = ARG.SOFTWARE_PACKAGE_ID AND SCTS.COMMAND_ID = ARG.COMMAND_ID AND SCTS.ARGUMENT_ID = ARG.ARGUMENT_ID".format(self.softwarePackageID,testSuitID,command)
		print(query)
		try:
			self.cursor.execute(query)
			data = self.cursor.fetchall()
		except MConn.Error as e:
			print("Error code: " + str(e.errno))
			print("Error Message: " + str(e.msg))
			print(str(e))
			return None
		else:
			return data
			
	def retreiveValuesForArguments(self):
		self.dictOfArgVal = {}
		self.dictOfArgVal2 = {}
		for argSet in self.dictOfCommandArguments:
			for eachArg in self.dictOfCommandArguments[argSet]:
				self.cursor.execute("select ARGUMENT_VAL_TYPE, DEFAULT_VALUE from ARGUMENT_VALUES WHERE ARGUMENT_ID = %s",(eachArg,))
				data = self.cursor.fetchall()
				listOfValues=[]
				#eachValType = [x[0] for x in data]
				#defVal = [x[1] for x in data]
				for eachValType, defVal in data:
					if eachValType in ['ABP','STR','NBR']:
						listOfValues.append(defVal)
					if eachValType == 'NSR' or eachValType == 'NER':
						print('NSR/NER')
						
					if eachValType == 'IMP':
						self.cursor.execute("select IMPORTS_FROM_COMMAND_ID, IMPORT_TAG from ARGUMENTS WHERE ARGUMENT_ID = %s and SOFTWARE_PACKAGE_ID = %s and COMMAND_ID = %s",[eachArg, self.softwarePackageID,argSet,])
						data1 = self.cursor.fetchall()
						for importFrom, importTag in data1:
							formatString = 'IMP{' + self.dictOfCommands[importFrom] + ',' + importTag+ '}'
						listOfValues.append(formatString)
					if eachValType == None:
						listOfValues.append('')
					
							
				self.dictOfArgVal[eachArg] = listOfValues
				self.dictOfArgVal2[eachArg] = data
			print("-----------------------------------------------")

	def createScripts(self,logFilePath,comSelect):
		self.outputLocation = createOutputLogDirectory(logFilePath)
		self.dictOfFileNames = {}
	
		for eachCommandID1 in comSelect:
			filename = createScript(self.dictOfCommands[eachCommandID1],self.outputLocation)
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
					
	def createScriptsForTestSuit(self,*args):
		print("In procedure to create test scripts for test suits")
		
		commandID = args[0]
		testSuitSelection = args[1]
		logFilePath = args[2]
		dictOfTestSuit = args[3]
		self.outputLocation = createOutputLogDirectory(logFilePath)
		self.dictOfFileNames = {}
		print("commandID: " + str(commandID))
		print("dictOfCommandArguments: ")
		print(self.dictOfCommandArguments)
		print("dictOfArguments")
		print(self.dictOfArguments)
		print('dictOfArgVal: ')
		print(self.dictOfArgVal)
		
		for eachTestSuit in testSuitSelection:
			filename = str(self.dictOfCommands[commandID]) + '_' + str(dictOfTestSuit[eachTestSuit])
			filenameCreated = createScript(filename,self.outputLocation)
			self.dictOfFileNames[eachTestSuit] = filenameCreated

		for eachTestSuitID in testSuitSelection:
			writeFile = open(self.dictOfFileNames[eachTestSuitID],'w')
			formatString = "{0} {1} ".format(self.softwarePackage,self.dictOfCommands[commandID])
			writeFile.write(formatString)
			writeFile.write('\n')
			data = self.fetchArgumentsForTestSuit(eachTestSuitID,commandID)
			length = 0
			dictData = {}
			
			if data is not None:
				argID = [x[0] for x in data]
				arguments = [x[1] for x in data]
				
			for eachArgID in argID:
				argString = 'Arg'+str(eachArgID)
				valueString = 'Value'+str(eachArgID)
				formatString = formatString + '{'+argString+'} {'+valueString+'} '
				dictData[argString] = self.dictOfArguments[eachArgID]
				if len(self.dictOfArgVal[eachArgID]) == 0:
					dictData[valueString] = ''
				elif len(self.dictOfArgVal[eachArgID]) == 1:
					dictData[valueString] = self.dictOfArgVal[eachArgID][0]
				else:
					dictData[valueString] = str(self.dictOfArgVal[eachArgID])
			print(formatString)
			print(formatString.format(**dictData))
			print('\n')
			print(dictData)
			formatString = formatString.format(**dictData)
			
			writeFile.write(formatString)
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
	

def generateScripts(*args):
	print("In proicedure to generate test suit scripts")
	argIDs = args[0],
	dictOfArguments = args[1]
	dictOfArgVal = args[2]
	formatString = args[3]
	dictData = {}
	for eachArgID in argIDs[0]:
		print(eachArgID)
		argString = 'Arg' + str(eachArgID)
		valueString = 'Value' + str(eachArgID)
		dictData[argString] = dictOfArguments[eachArgID]
		if len(dictOfArgVal[eachArgID]) == 0:
			dictData[valueString] = ''
		elif len(dictOfArgVal[eachArgID]) == 1:
			dictData[valueString] = dictOfArgVal[eachArgID][0]
		else:
			dictData[valueString] = str(dictOfArgVal[eachArgID])
	print(dictData)
	print(formatString.format(**dictData))