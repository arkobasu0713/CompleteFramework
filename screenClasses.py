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


class CreateCommandScreen(Screen):
	pass
	def __init__(self,**kwargs):
		super(CreateCommandScreen,self).__init__(**kwargs)
		self.hasMand = 0
		self.hasOpt = 0

	def addArgument(self):
		print("Popup for adding argument")


	def saveCommand(self):
		commandName = self.ids.id_command_name_entry_CCS.text
		if commandName != '':
			ret = DBConn.processNewEntryCommand(commandName,conn,self.hasMand,self.hasOpt)
			print(ret)
			if ret == 'Success':
				popup = UTIL.createP1('Success','Create Command','Successful transaction on table SOFTWARE_COMMANDS for creating Command')
				popup.open()
			else:
				popup = UTIL.createP1('Failure','Create Command','Unsuccessful transaction on table SOFTWARE_COMMANDS',ret)
				popup.open()
		else:
			print("Enter command name")


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
		ret = DBConn.deleteCommand(conn,self.commandList,conn.softwarePackageID)
		if ret == 'Success':
			popup = UTIL.createP1('Success','Delete Command','Successful Deletion of Command')
			popup.open()
		else:
			popup = UTIL.createP1('Failure','Delete Command','Unable to delete command',ret)
			popup.open()

		

	def selectCommand(self,*args):
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
			
	def query(self,*args):
		self.ids.boxToDisplayArgumentDetailsID.clear_widgets()
		conn.fetchArgumentsForSelectCommands(self.commandList)
		conn.retreiveValuesForArguments()
		print(conn.dictOfCommandArguments)
		print('\n')
		print(conn.dictOfArgVal)
		print('\n')
		print(conn.dictOfArguments)
		print('\n')
		print(conn.dictOfArgVal2)
		print('\n')
		print(conn.dictOfCommands)
#		for eachArg in conn.dictOfArguments:
#			idString = "label_id_"+str(eachArg)+"_Edit_Screen"
		label_str = "{numberOfArguments} Arguments Found".format(numberOfArguments=len(conn.dictOfArguments))
		label_tmp = Label(text=label_str,background_color=(1,1,0,1),multiline=True)
		self.ids.boxToDisplayArgumentDetailsID.add_widget(label_tmp)
		if len(conn.dictOfArguments) > 0:
			self.ids.diplayArgDetailButtonID.disabled = False
		
	def displayDetail(self):
		pop = UTIL.createP1("Arguments. Click them to veiw/modify their values","Display Argument Details","",conn.dictOfArguments,conn.dictOfCommands,conn,conn.dictOfArgVal)
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
		self.mapDriveAt = ''
		self.logFilePath = ''
		self.folderName = ''
		
		conn.retreiveCommandsUnderSoftwarePackage(conn.softwarePackageID)

		self.ids.grid_id_commands_DPDS.clear_widgets()
		for eachCommand in conn.dictOfCommands:
			idString = "button_id_" +str(eachCommand) + "_DPDS"
			btn_temp = UTIL.myButton(text=conn.dictOfCommands[eachCommand], id=idString, background_color= (1,1,0,1))
			self.ids.grid_id_commands_DPDS.add_widget(btn_temp)
			btn_temp.bind(on_press=Par(self.addSelection, eachCommand,idString))
		
	
	def setTrueAll(self,*args):
		if self.ids.id_checkBox_DPDS.state == 'down':
			self.runScript = 'Y'
		else:
			self.runScript = 'N'

		
	def addSelection(self,*args):
		print("Selection: " + str(args[0]))
		self.comSelect.append(args[0])
		self.buttonIDList.append(args[1])

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

	def refreshContents(self):
		conn.reEstablishConnection()
		conn.retreiveCommandsUnderSoftwarePackage(conn.softwarePackageID)

		self.ids.grid_id_commands_DPDS.clear_widgets()
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

