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
		commandString = "net use q: \\nserver.hgst.com\ISOs\iso2usb"

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
	print("Display pop-up for commands")
	
def addValues(*args):
	print("Display pop-up for adding arguments")

def createP1(*args):
	stat = args[0]
	popupTitle = args[1]
	
	mainBox = BoxLayout(orientation='vertical')
	label = Label(text=stat, color=(1,0,0,1),size_hint=(1,.15))
	innerButtonControlBox = BoxLayout(orientation='horizontal', size_hint=(1,.15))
	btn_ok = Button(text='Ok',background_color=(1,0,0,1))
	

	innerButtonControlBox.add_widget(btn_ok)
	mainBox.add_widget(label)
	
	if stat == 'Failure':
		err = args[2]
		label2 = Label(text=str(err.msg),multiline=True,color=(1,0,0,1))
		mainBox.add_widget(label2)
		
	if popupTitle == 'Argument Details':
		gridlayout = GridLayout(cols=2)
		for eachArg in args[2]:
			string = "Argument:  {arg}\nArgument Values: ".format(arg=args[2][eachArg])
			label = Label(text=string,multiline=True,color=(1,0,0,1))
			gridlayout.add_widget(label)
		mainBox.add_widget(gridlayout)

	if popupTitle == 'Add Argument':
		gridlayout = GridLayout(cols=2)
		label1 = Label(text="Argument Description: ",color=(1,0,0,1))
		gridlayout.add_widget(label1)
		txtInpt = TextInput(id='textInputForArgumentID')
		gridlayout.add_widget(txtInpt)
		btn = Button(text="Click if it imports data from another command",font_size=10)
		gridlayout.add_widget(btn)
		btn.bind(on_press=Par(displayCommands))
		btn_val = Button(text="Click to add Values to the argument",font_size=10,id='valButtonID')
		gridlayout.add_widget(btn_val)
		btn_val.bind(on_press=Par(addValues))
		mainBox.add_widget(gridlayout)
		
	
	mainBox.add_widget(innerButtonControlBox)

	popup1 = Popup(title=popupTitle, content=mainBox, size_hint=(None,None), size=(550,500), auto_dismiss=False)
	btn_ok.bind(on_press=popup1.dismiss)
	
	return popup1
