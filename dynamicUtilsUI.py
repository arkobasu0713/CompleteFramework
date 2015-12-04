import os
import sys
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
from screenClasses import *
import argparse
import sys
import os
import time
import platform
import subprocess
import shutil

def mappingNetworkDrive():
	print("Current OS the script is running on: " + str(platform.system()))
	if platform.system() == 'Windows':
		
		#formatting the command string for mapping the network drive
		commandString = "net use q: \\\\nserver.hgst.com\ISOs\iso2usb"

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
			return ''
		else:
			print("Mapping network drive was successful")
			return "q:"


	elif platform.system() == 'Linux':
		
		#formatting the command string for mapping the network drive
		commandString = "mount -t cifs -w //nserver.hgst.com/ISOs/iso2usb"
		print("Creating mount location within directory structure.")
		mountLocation = os.path.join(os.getcwd(),("mountLocation"+str(time.strftime("%Y-%m-%d"))))
		print("Mount location being used: " + mountLocation)
		commandString = commandString + " " + mountLocation
		if not os.path.exists(mountLocation):
			print("Path doesn't exist. Creating Mount location")
			try:
				os.mkdir(mountLocation)
			except OSError as exc:
				if exc.errno == errno.EEXIST and os.path.isdir(mountLocation):
					pass
				else: raise
		print("Mounting network drive with default values") #needs to be worked upon
		commandString = commandString + " -o username=disty,password=sitlab"
		
		print("Cmd String: " + commandString)
		p = subprocess.Popen(commandString,shell=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
		output, err = p.communicate()
		if output.decode('ascii') == '' and err.decode('ascii') == '':
			print("Mapping network drive was successful")
			return mountLocation
		else:
			print("Mapping network drive was unsuccessful")
			print(err.decode('ascii'))
			return ''

	else:
		print("The script is being tried to run on a platform outside the scope of the covergae of this tool. Please note that mapping the network drive would not be possible")
		return ''
	


def fetchLogFilePath():
	logFilePath = os.path.join(os.path.dirname(__file__),'DefaultLogFilePath')
	if not os.path.exists(logFilePath):
		print("Default directory for storing log files are not found.Creating.")		
		os.mkdir(logFilePath)
	else:
		print("Default directory for storing log files found. Located at: " + logFilePath)

	return logFilePath

def backApp(*args):
	args[0].current = 'ApplicationConsole'

def backApp1(*args):
	args[0].current = 'DisplayPackagesDetailsScreen'

def end(self,*args):
	sys.exit(0)

def changeScreen(self,*args):
	args[0].current = 'WelcomeScreen'

def createPopupExit(sm):
	box = BoxLayout()
	btn1 = Button(text='Yes')
	btn2 = Button(text='No. Take me back.')
	btn1.bind(on_press=end)
	box.add_widget(btn1)
	box.add_widget(btn2)
	popup = Popup(title='Confirm Exit', content=box,size_hint=(None,None), size=(400,100), auto_dismiss=False)
	btn2.bind(on_press=popup.dismiss)
	btn2.bind(on_press=Par(changeScreen,sm))

	return popup

def createPopupWidget1(sm,msg):

	
	mainBox = BoxLayout(orientation='vertical')
	label = Label(text=msg, color=(1,0,0,1))
	innerButtonControlBox = BoxLayout(orientation='horizontal', size_hint=(1,.25))
	btn_ok = Button(text='Ok. Take me back to App Screen',background_color=(1,0,0,1), size_hint=(.7,1))
	
	innerButtonControlBox.add_widget(btn_ok)
	
	mainBox.add_widget(label)
	mainBox.add_widget(innerButtonControlBox)

	popup1 = Popup(title='Processing Soft Package', content=mainBox, size_hint=(None,None), size=(550,500), auto_dismiss=False)
	btn_ok.bind(on_press=popup1.dismiss)
	btn_ok.bind(on_press=Par(backApp,sm))
	
	return popup1

def createPopupWidget2(sm,dictOfStatus,size):

	mainBox = BoxLayout(orientation='vertical',id="mainBox")
	mainBox.clear_widgets()
	label = Label(text='Completed',color=(1,0,0,1),size_hint=(1,.3),id="label")
	mainBox.add_widget(label)
	for eachScript in dictOfStatus:
		textContent = "Filename containing scripts: " + os.path.basename(eachScript) + '\n' + "Total number of scripts generated: " + str((dictOfStatus[eachScript])[2]) +'\n' +"Number of Scripts that ran to success: " + str((dictOfStatus[eachScript])[0]) + '\n' + "Number of Scripts that did not run:    " + str((dictOfStatus[eachScript])[1]) + '\n\n'
		labelScript = Label(text=textContent,multiline=True,color=(1,0,0,1))
		mainBox.add_widget(labelScript)

	innerButtonControlBox = BoxLayout(orientation='horizontal', size_hint=(1,.25))
	btn_ok = Button(text='Ok. Take me back to Run Control Screen',background_color=(1,0,0,1), size_hint=(.6,1))
	btn_cancel = Button(text='Cancel',background_color=(1,0,0,1),size_hint=(.2,1))
	innerButtonControlBox.add_widget(btn_ok)
	innerButtonControlBox.add_widget(btn_cancel)

	
	mainBox.add_widget(innerButtonControlBox)

	popup1 = Popup(title='Status of test suits run screen', content=mainBox, size_hint=(None,None), size=size, auto_dismiss=False)
	btn_ok.bind(on_press=popup1.dismiss)
	btn_ok.bind(on_press=Par(backApp1,sm))
	btn_cancel.bind(on_press=popup1.dismiss)
	btn_cancel.bind(on_press=Par(backApp1,sm))

	return popup1
	
def displayCommands(*args):
	popupNew = createP1("Select the Command from the below list that the argument imports data from","Commands",args[0])
	popupNew.open()
		
def addValues(*args):
	print("Display pop-up for adding arguments")
	
def displayArgumentDetails(*args):
	print("Display pop-up for each argument details with control of modifying them")
	
def processArgEntry(*args):
	print(args[0])
	print(args[1])
	DBConn.processArgEntry()
	
def disableOthers(*args):
	gridlayout = args[0]
	gridIDPopUP = args[1]
	idString = args[2]
	for children in gridlayout.children:
		if children.id != idString:
			if children.disabled == True:
				children.disabled = False
			else:
				children.disabled = True
				
def validateCommandImport(*args):
	print("Validate import procedure")
	

def createP1(*args):
	stat = args[0]
	popupTitle = args[1]
	
	mainBox = BoxLayout(orientation='vertical',id="mainBoxID")
	label = Label(text=stat, color=(1,1,0,1),size_hint=(1,.15),id="labelID")
	innerButtonControlBox = BoxLayout(orientation='horizontal', size_hint=(1,.15),id="innerButtonControlBoxID")
	btn_ok = Button(text='Ok',background_color=(1,0,0,1),id="btn_okID")
	

	innerButtonControlBox.add_widget(btn_ok)
	mainBox.add_widget(label)
	
	if stat == 'Failure':
		err = args[2]
		label2 = Label(text=str(err.msg),multiline=True,color=(1,0,0,1),id="label2ID")
		mainBox.add_widget(label2)
		
	if popupTitle == 'Argument Details':
		gridlayout = GridLayout(cols=2,id="gridlayoutID")
		for eachArg in args[2]:
			string = "{arg}".format(arg=args[2][eachArg])
			btn = Button(text=string,id=str("btn"+str(args[2][eachArg])+"ID"))
			gridlayout.add_widget(btn)
			btn.bind(on_press=Par(displayArgumentDetails))
		mainBox.add_widget(gridlayout)

	if popupTitle == 'Add Argument':
		gridlayout = GridLayout(cols=2,id="gridlayoutID",size_hint=(1,.5))
		label1 = Label(text="Argument Description: ",color=(1,0,0,1),id="label1ID")
		gridlayout.add_widget(label1)
		txtInpt = TextInput(id='textInputForArgumentID')
		gridlayout.add_widget(txtInpt)
		btn = Button(text="Click if it imports data from another command",font_size=10,id="btnID")
		gridlayout.add_widget(btn)
		btn.bind(on_press=Par(displayCommands,args[2]))
		btn_val = Button(text="Click to add Values to the argument",font_size=10,id='valButtonID')
		gridlayout.add_widget(btn_val)
		btn_val.bind(on_press=Par(addValues))
		mainBox.add_widget(gridlayout)
		btn_save = Button(text="Save to DB",background_color=(1,0,0,1),id="buttonSaveID")
		innerButtonControlBox.add_widget(btn_save)
		btn_save.bind(on_press=Par(DBConn.processArgEntry,txtInpt,args[3],args[4]))
		
		
	if popupTitle == 'Commands':
		gridlayout = GridLayout(cols=3,id="gridIDPopUP")
		for eachCommand in args[2]:
			idString = "button_id_" +str(eachCommand) + "_EDITScreen"
			btn_tmp = myButton(text=conn.dictOfCommands[eachCommand], id=idString, background_color= (1,1,0,1))
			gridlayout.add_widget(btn_tmp)
			btn_tmp.bind(on_press=Par(disableOthers,gridlayout,"gridIDPopUP",idString))
		mainBox.add_widget(gridlayout)
		gridlayout2 = GridLayout(cols=2,size_hint=(1,.3),id="gridlayout2ID")
		labelImport = Label(text="Import Tag: ",color=(1,0,0,1),id="labelImportID")
		txtInpt2 = TextInput(id="textInputForImportTagID")
		gridlayout2.add_widget(labelImport)
		gridlayout2.add_widget(txtInpt2)
		mainBox.add_widget(gridlayout2)
		
	
	btn_cancel = Button(text="Cancel",background_color=(1,0,0,1),id="buttonCanID")
	innerButtonControlBox.add_widget(btn_cancel)
	mainBox.add_widget(innerButtonControlBox)

	popup1 = Popup(title=popupTitle, content=mainBox, size_hint=(None,None), size=(550,500), auto_dismiss=False,id="Popup1ID")
	btn_ok.bind(on_press=Par(validateCommandImport,popup1))
	btn_ok.bind(on_release=popup1.dismiss)
	btn_cancel.bind(on_press=popup1.dismiss)
	
	return popup1
	
class myButton(Button):
	background_color_normal = list([.5,.2,.2,1])
	background_color_down = list([1,0,.5,1])

	def __init__(self,**kwargs):
		super(myButton,self).__init__(**kwargs)
		self.background_normal = ""
		self.background_down = ""
		self.background_color = self.background_color_normal
	def on_press(self):
		if self.background_color == self.background_color_down:
			self.background_color = self.background_color_normal
		else:
			self.background_color = self.background_color_down