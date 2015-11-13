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


class MyCustomPopupWidget(Popup):
	pass
	def __init__(self,**kwargs):
		super(MyCustomPopupWidget,self).__init__(**kwargs)
		print("In myCustomPopupWidget")

	def on_press_ok(self,*args):
		self.dismiss
		UTIL.backApp(sm)

class CreateArgumentScreen(Screen):
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
			UTIL.processNewEntrySoftPackage(softwarePackageName,softwarePackageLocation)
			customPopWidget = UTIL.createPopupWidget1(sm,'Success')
			customPopWidget.open()
		else:
			print("Enter software package details")
			customPopWidget = UTIL.createPopupWidget1(sm,'Wrong Try')
			customPopWidget.open()


	def mapDrive(self):
		mapDriveAt = UTIL.mappingNetworkDrive()
		if mapDriveAt != '':
			print("It has been mapped at: " + mapDriveAt)

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

class myButton(Button):
	background_color_normal = list([.5,.2,.2,1])
	background_color_down = list([1,0,.5,1])

	def __init__(self,**kwargs):
		super(myButton,self).__init__(**kwargs)
		self.background_normal = ""
		self.background_down = ""
		self.background_color = self.background_color_normal
	def on_press(self):
		self.background_color = self.background_color_down

class DisplayPackagesDetailsScreen(Screen):
	
	def __init__(self,**kwargs):
		super(DisplayPackagesDetailsScreen,self).__init__(**kwargs)
		self.buttonIDList = []
		self.runScript = 'N'

		self.comSelect = []
		
		conn.retreiveCommandsUnderSoftwarePackage(conn.softwarePackageID)

		self.ids.grid_id_commands_DPDS.clear_widgets()
		for eachCommand in conn.dictOfCommands:
			idString = "button_id_" +str(eachCommand) + "_DPDS"
			btn_temp = myButton(text=conn.dictOfCommands[eachCommand], id=idString, background_color= (1,1,0,1))
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


		
	def runCommandSuits(self):
		logFilePath = self.ids.id_logpath_DPDS.text
		if logFilePath == "":
			logFilePath = UTIL.fetchLogFilePath()
		
		
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
		print("Creating folder under mapped network drive with software package name")

	def mapNetworkDrive(self):
		if mapDriveAt != '':
			mapDriveAt = UTIL.mappingNetworkDrive()
			if mapDriveAt != '':
				print("It has been mapped at: " + mapDriveAt)

			


	def callback(self):
		sm.add_widget(DisplayResultsScreen(name='DisplayResultsScreen'))
		sm.current = 'DisplayResultsScreen'
		
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

