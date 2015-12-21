#Author: 11/10/2015
import sys
import time
import kivy
import datetime
import time
import os
from random import randint
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Color
from kivy.graphics.instructions import Canvas
import dataConnect as DBConn
from functools import partial as Par
from kivy.uix.popup import Popup
import dynamicUtilsUI as UTIL

global conn
conn = DBConn.enterDBSpace()
sm = ScreenManager()
global mapDriveAt
mapDriveAt = ''

class EditCommandScreen(Screen):
	def __init__(self,**kwargs):
		super(EditCommandScreen,self).__init__(**kwargs)

		conn.retreiveCommandsUnderSoftwarePackage(conn.softwarePackageID)
		self.ids.deleteButtonID.disabled = True
		self.ids.diplayArgDetailButtonID.disabled = True
		self.ids.displayArgumentID.disabled = True
		self.ids.addArgumentButtonID.disabled = True
		self.commandList = []

		self.ids.grid_id_commands_ECS.clear_widgets()
		for eachCommand in conn.dictOfCommands:
			idString = "button_id_" +str(eachCommand) + "_DPDS"
			btn_temp = UTIL.myButton(text=conn.dictOfCommands[eachCommand], id=idString, background_color= (1,1,0,1))
			self.ids.grid_id_commands_ECS.add_widget(btn_temp)
			btn_temp.bind(on_press=Par(self.selectCommand,eachCommand,idString))

	def editCommand(self,*args):
		self.ids.deleteButtonID.disabled = False

	def delete(self,*args):
		conn.fetchArgumentsForSelectCommands(self.commandList)
		conn.retreiveValuesForArguments()
		ret, flag1, flag2, flag3, e = DBConn.deleteCommand(conn,self.commandList,conn.softwarePackageID)
		if ret == 1:
			popup = UTIL.createP1('Success','Successful deletion',"Transaction for specified commands on ARGUMENTS, ARGUMENT_VALUES, and SOFTWARE_COMMANDS successful")
			popup.open()
		else:
			if flag1 != 1:
				popupFailure = UTIL.createP1('Failure','Unsuccessful Argument Value Deletion',"Unsuccessful transaction on table ARGUMENT_VALUES",e)
			elif flag2 != 1:
				popupFailure = UTIL.createP1('Failure','Unsuccessful Argument Deletion',"Successful Transaction on ARGUMENT_VALUES but, Unsuccessful transaction on table ARGUMENTS",e)
			elif flag3 != 1:
				popupFailure = UTIL.createP1('Failure','Unsuccessful Command Deletion',"Successful Transaction on ARGUMENTS and ARGUMENT_VALUES but, Unsuccessful transaction on table SOFTWARE_COMMANDS",e)
			popupFailure.open()

	def selectCommand(self,*args):
		print("In selectCommand: ")
		if args[0] not in self.commandList:
			self.commandList.append(args[0])
		else:
			self.commandList.remove(args[0])
		print(self.commandList)
		if len(self.commandList) > 0:
			self.ids.deleteButtonID.disabled = False
		else:
			self.ids.deleteButtonID.disabled = True		

		if len(self.commandList) == 1:
			self.ids.displayArgumentID.disabled = False
			self.ids.addArgumentButtonID.disabled = False
			#self.ids.diplayArgDetailButtonID.disabled = False
		else:
			self.ids.displayArgumentID.disabled = True
			self.ids.addArgumentButtonID.disabled = True
			self.ids.diplayArgDetailButtonID.disabled = True
			self.ids.boxToDisplayArgumentDetailsID.clear_widgets()
			
	def query(self,*args):
		self.ids.boxToDisplayArgumentDetailsID.clear_widgets()
		conn.fetchArgumentsForSelectCommands(self.commandList)
		conn.retreiveValuesForArguments()
		#print(conn.dictOfCommandArguments)
		#print('\n')
		#print(conn.dictOfArgVal)
		#print('\n')
		#print(conn.dictOfArguments)
		#print('\n')
		#print(conn.dictOfArgVal2)
		#print('\n')
		#print(conn.dictOfCommands)
		label_str = "{numberOfArguments} Arguments Found".format(numberOfArguments=len(conn.dictOfArguments))
		label_tmp = Label(text=label_str,background_color=(1,1,0,1),multiline=True)
		self.ids.boxToDisplayArgumentDetailsID.add_widget(label_tmp)
		if len(conn.dictOfArguments) > 0:
			self.ids.diplayArgDetailButtonID.disabled = False
		
	def displayDetail(self):
		pop = UTIL.createP1("Arguments. Click them to veiw/modify their values","Display Argument Details","",conn.dictOfArguments,conn.dictOfCommands,conn,conn.dictOfArgVal,self.commandList)
		pop.open()
		
	def addArgument(self):
		pop = UTIL.createP1("Add argument values below","Add Argument","",conn.dictOfCommands,self.commandList[0],conn)
		pop.open()
		
	def refreshContents(self):
		conn.reEstablishConnection()
		conn.retreiveCommandsUnderSoftwarePackage(conn.softwarePackageID)
		self.commandList = []
		self.ids.deleteButtonID.disabled = True
		self.ids.displayArgumentID.disabled = True
		self.ids.diplayArgDetailButtonID.disabled = True
		self.ids.addArgumentButtonID.disabled = True
		
		self.ids.grid_id_commands_ECS.clear_widgets()
		self.ids.boxToDisplayArgumentDetailsID.clear_widgets()
		for eachCommand in conn.dictOfCommands:
			idString = "button_id_" +str(eachCommand) + "_EditScreen"
			btn_temp = UTIL.myButton(text=conn.dictOfCommands[eachCommand], id=idString, background_color= (1,1,0,1))
			self.ids.grid_id_commands_ECS.add_widget(btn_temp)
			btn_temp.bind(on_press=Par(self.selectCommand,eachCommand,idString))

class EditTestSuitScreen(Screen):
	pass

class WelcomeScreen(Screen):
	pass
	def quit(self):
		popup = UTIL.createPopupExit(sm)
		popup.open()	

class CreateScreen(Screen):
	def __init__(self,**kwargs):
		super(CreateScreen,self).__init__(**kwargs)


	def createEntry(self):
		softwarePackageName = self.ids.softPackage_desc_entry_feild_id_CS.text
		softwarePackageLocation = self.ids.softPackage_url_repo_entry_feild_id_CS.text
		if softwarePackageName != '':
			DBConn.processNewEntrySoftPackage(softwarePackageName,softwarePackageLocation,conn)
			customPopWidget = UTIL.createPopupWidget1(sm,'Success')
			customPopWidget.open()
		else:
			print("Enter software package details")
			customPopWidget = UTIL.createPopupWidget1(sm,'Wrong Try')
			customPopWidget.open()


	def createRootDirectory(self):
		if self.mapDriveAt == '':
			print("Please click on the Map Network Drive first to map the default network drive first.")
		else:
			softwarePackageName = self.ids.softPackage_desc_entry_feild_id_CS.text
			softwarePackageLocation = self.ids.softPackage_url_repo_entry_feild_id_CS.text
			print("Create a folder under root directory with software package name")

class ApplicationControlScreen(Screen):
	pass
	def __init__(self,**kwargs):
		super(ApplicationControlScreen,self).__init__(**kwargs)

	def fetchAndChangeScreen(self):
		sm.current = 'DisplayResultsScreen'

class CreateNewTestSuitScreen(Screen):
	pass
	
def selectTestSuit(*args):
	testSuitID = args[0]
	testSuitSelection = args[1]
	commandID = args[2]
	if testSuitID in testSuitSelection:
		testSuitSelection.remove(testSuitID)
	else:
		testSuitSelection.append(testSuitID)

	print("In procedure of selecting test suits: ")
	print(testSuitSelection)
	
class DisplayPackagesDetailsScreen(Screen):
	
	def __init__(self,**kwargs):
		super(DisplayPackagesDetailsScreen,self).__init__(**kwargs)
		self.buttonIDList = []
		self.runScript = 'N'
		self.ids.label_id1_DPDS.text = 'Commands and Test Suits for software package: ' + conn.softwarePackage
		self.comSelect = []
		self.ids.createTestSuitID.disabled = True
		self.ids.editTestSuitID.disabled = True
		self.ids.button_id3_DPDS.disabled = True
		self.ids.id_checkBox_DPDS.state = 'down'
		self.mapDriveAt = ''
		self.logFilePath = ''
		self.folderName = ''
		self.testSuitSelection = [] 
		self.commandID = ''
		
		conn.retreiveCommandsUnderSoftwarePackage(conn.softwarePackageID)
		
		self.ids.grid_id_customTestSuit_DPDS.clear_widgets()

		self.ids.grid_id_commands_DPDS.clear_widgets()
		for eachCommand in conn.dictOfCommands:
			idString = "button_id_" +str(eachCommand) + "_DPDS"
			btn_temp = UTIL.myButton(text=conn.dictOfCommands[eachCommand], id=idString, background_color= (1,1,0,1))
			self.ids.grid_id_commands_DPDS.add_widget(btn_temp)
			btn_temp.bind(on_press=Par(self.addSelection, eachCommand,idString))
		
	
	def setTrueAll(self,*args):
		if self.ids.id_checkBox_DPDS.state != 'down':
			self.runScript = 'Y'
		else:
			self.runScript = 'N'
		
	def addSelection(self,*args):
		commandID = args[0]
		print("Selection: " + str(commandID))
		if commandID in self.comSelect:
			self.comSelect.remove(commandID)
			self.buttonIDList.remove(args[1])
		else:
			self.comSelect.append(commandID)
			self.buttonIDList.append(args[1])
		
		self.ids.grid_id_customTestSuit_DPDS.clear_widgets()
		if commandID in self.comSelect:
			self.commandID = commandID
			data = conn.fetchTestSuits(commandID)
			if data is not None:
				for eachDataSet in data:
					testSuitID = eachDataSet[0]
					testSuitName = eachDataSet[1]
					btn = UTIL.myButton(text=testSuitName,color=(1,0,0,1),id=str(testSuitID))
					self.ids.grid_id_customTestSuit_DPDS.add_widget(btn)
					btn.bind(on_press=Par(selectTestSuit,testSuitID,self.testSuitSelection))
		else:
			self.commandID = ''
		
	def addCommand(self,*args):
		print("Generating popup for creating command")
		popup = UTIL.createP1('Add Command details below','Create Command','',conn)
		popup.open()

	def mapDrive(self):
		self.mapDriveAt = UTIL.mappingNetworkDrive()
		if self.mapDriveAt != '':
			print("It has been mapped at: " + self.mapDriveAt)
			self.ids.button_id3_DPDS.disabled = False
		else:
			print("Mapping Error")
		
	def runCommandSuits(self):
		logFilePath = self.ids.id_logpath_DPDS.text
		if logFilePath == "":
			logFilePath = UTIL.fetchLogFilePath()
		if self.mapDriveAt != '':
			logFilePath = self.folderName
		print(logFilePath)
		
		
		conn.fetchArgumentsForSelectCommands(self.comSelect)
		conn.retreiveValuesForArguments()
		conn.createScripts(logFilePath,self.comSelect)
		if self.runScript == 'Y':
			dictOfStatus = conn.runScripts()
			createPopupDetails = UTIL.createPopupWidget2(sm,dictOfStatus,self.size)
			createPopupDetails.open()


		for children in self.ids.grid_id_commands_DPDS.children:
			if children.id in self.buttonIDList:
				children.background_color = (.5,.2,.2,1)
		del self.comSelect[:]
		del self.buttonIDList[:]

	def createFolder(self):
		self.folderName = ''
		print("Creating folder under mapped network drive with software package name")
		print("Creating folder inside the mapped directory in the format software_package_name_TestSuit_yyyymmdd")
		folderName = conn.softwarePackage + "TestSuit" + str(time.strftime("%Y-%m-%d"))
		absolutePathofFolderName = os.path.join(self.mapDriveAt,folderName)
		if not os.path.exists(absolutePathofFolderName):
			os.makedirs(absolutePathofFolderName)
			print("Folder created at : " + absolutePathofFolderName)
			self.folderName = absolutePathofFolderName
		else:
			print("Folder already exists")
			self.folderName = absolutePathofFolderName
		
	def callback(self):
		sm.add_widget(DisplayResultsScreen(name='DisplayResultsScreen'))
		sm.current = 'DisplayResultsScreen'

	def goToEditScreen(self):
		sm.add_widget(EditCommandScreen(name='EditCommandScreen'))
		sm.current = 'EditCommandScreen'
		
	def runTestSuits(self):
		print("In procedure to run for selected test suits")
		print(self.testSuitSelection)
		print(self.commandID)

	def refreshContents(self):
		conn.reEstablishConnection()
		conn.retreiveCommandsUnderSoftwarePackage(conn.softwarePackageID)

		self.ids.grid_id_commands_DPDS.clear_widgets()
		self.ids.grid_id_customTestSuit_DPDS.clear_widgets()
		for eachCommand in conn.dictOfCommands:
			idString = "button_id_" +str(eachCommand) + "_DPDS"
			btn_temp = UTIL.myButton(text=conn.dictOfCommands[eachCommand], id=idString, background_color= (1,1,0,1))
			self.ids.grid_id_commands_DPDS.add_widget(btn_temp)
			btn_temp.bind(on_press=Par(self.addSelection, eachCommand,idString))
		
class DisplayResultsScreen(Screen):
	def __init__(self,**kwargs):
		super(DisplayResultsScreen,self).__init__(**kwargs)
		conn.fetchSoftPackage()

		for softPackageID in conn.dictOfPackages:
			btn = Button(text=conn.dictOfPackages[softPackageID], id=str(softPackageID), size_hint=(1,.2), background_color= (1,1,0,1))
			self.ids.innerBoxForSoftwarePackageButton_id_DRS.add_widget(btn)
			btn.bind(on_press=Par(self.enterPackage,softPackageID,conn.dictOfPackages[softPackageID]))
			
	def refresh(self):
		conn.reEstablishConnection()
		conn.fetchSoftPackage()
		print(conn.dictOfPackages)
		self.ids.innerBoxForSoftwarePackageButton_id_DRS.clear_widgets()
		for softPackageID in conn.dictOfPackages:
			btn = Button(text=conn.dictOfPackages[softPackageID], id=str(softPackageID), size_hint=(1,.15), background_color= (1,1,0,1))
			self.ids.innerBoxForSoftwarePackageButton_id_DRS.add_widget(btn)
			btn.bind(on_press=Par(self.enterPackage,softPackageID,conn.dictOfPackages[softPackageID]))
		

	def backScreen(self,*args):
		self.manager.current = 'ApplicationConsole'
	
	def enterPackage(self,*args):
		conn.softwarePackage = args[1]
		conn.softwarePackageID = args[0]
		sm.switch_to(DisplayPackagesDetailsScreen(name='DisplayPackagesDetailsScreen'))

