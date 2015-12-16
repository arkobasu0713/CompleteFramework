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
from kivy.uix.dropdown import DropDown
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
		commandString = "net use q: \\\\nserver.hgst.com\softwaretoolstest"

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
			if 'SYSTEM ERROR 85' in(err.decode('ascii')).upper():
				return 'q:'
			else:
				return ''
		else:
			print("Mapping network drive was successful")
			return "q:"


	elif platform.system() == 'Linux':
		
		#formatting the command string for mapping the network drive
		commandString = "mount -t cifs -w //nserver.hgst.com/softwaretoolstest"
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
		commandString = commandString + " -o username=abasu,password=disco1234"
		
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
	dictOfCommands = args[0]
	btn = args[1]
	txtInptImport = args[2]
	btn_val = args[3]
	popupNew, grid = createP1("Command Import","Commands","Select the Command from the below list that the argument imports data from",dictOfCommands)
	popupNew.open()
	par = Par(validateCommandImport,grid, btn, txtInptImport,dictOfCommands,btn_val)
	popupNew.bind(on_dismiss=par)
		
		

def addValues(*args):
	print("Display pop-up for adding argument values")
	popup = createP1("Enter Argument values","Add Values","You can add multiple values under this screen")
	popup = popup.open()
	
def displayArgumentDetails(*args):
	print("Display pop-up for each argument details with control of modifying them")
	btn=args[0]
	
def disableOthers(*args):
	gridlayout = args[0]
	idString = args[1]
	for children in gridlayout.children:
		if children.id != idString:
			if children.disabled == True:
				children.disabled = False
			else:
				children.disabled = True

def enableAll(*args):
	grid = args[0]
	for children in grid.children:
		children.disabled = False
		
def validateCommandImport(*args):
	print("Validate import procedure")
	gridLayout = args[0]
	btn = args[1]
	btn_val = args[4]
	count = 0
	child = None
	dictOfCommands = args[3]
	txtInptImport = args[2]
	for children in gridLayout.children:
		if children.disabled == False:
			count = count + 1
			child = children
	if count == 1:
		print(child)
		print("Commandid: " + child.id)
		btn.background_color = list([1,0,.5,1])
		btn.id = child.id
		print(dictOfCommands[int(child.id)])
		btn.text = "Imports data from Command ID: {} ({})".format(child.id,dictOfCommands[int(child.id)])
		txtInptImport.disabled = False
		btn_val.disabled = True
	else:
		btn.background_color = list([1,1,1,1])
		txtInptImport.text = ""
		txtInptImport.disabled = True
		btn_val.disabled = False
		btn.id = "valButtonID"
		btn.text = "Click if it imports data from another command"
		btn.font_size = 12
		
def addArgSection(*args):
	grid = args[0]
	
def editSelection(*args):
	print("In Edit Selection")
	popup = createP1("Enter Argument values","Add Values","You can add multiple values under this screen")
	popup = popup.open()
	
	
def selectArg(*args):
	#print("In Select Argument inside popup")
	btn = args[0]
	selection = args[1]
	btn_edit = args[2]
	btn_sub = args[3]
	if btn.id not in selection:
		selection.append(btn.id)
	else:
		selection.remove(btn.id)
	#print(selection)
		
	if len(selection) == 1:
		btn_edit.disabled = False
		btn_sub.disabled = False
	elif len(selection) > 1:
		btn_edit.disabled = True
		btn_sub.disabled = False
	else:
		btn_edit.disabled = True
		btn_sub.disabled = True
		
def addDetails(*args):
	print("In procedure to add details")
	gridlayout = args[0]
	label = Label(text="Argument Value Type: ",color=(1,0,0,1))
	label2 = Label(text="Default Argument Parameter: ",color=(1,0,0,1))
	label3 = Label(text="Default Value",color=(1,0,0,1))
	textInput = TextInput(id="textInputIDForDefaultArgParameter")
	textInput2 = TextInput(id="textInputIDForDefaultValue")
	gridlayout.add_widget(label)
	btnMain = Button(text="ValueType",id="valueTypeID")	
	gridlayout.add_widget(btnMain)
	gridlayout.add_widget(label2)
	gridlayout.add_widget(textInput)
	gridlayout.add_widget(label3)
	gridlayout.add_widget(textInput2)
	kindOfValues = ['NULL','ABP','NUMR','STR']
	dropdown = DropDown()
	for eachType in kindOfValues:
		btn_tmp = Button(text=eachType, size_hint_y=None, height=20)
		btn_tmp.bind(on_release=lambda btn_tmp: dropdown.select(btn_tmp.text))
		dropdown.add_widget(btn_tmp)
			
	btnMain.bind(on_release=dropdown.open)
	dropdown.bind(on_select=lambda instance, x: setattr(btnMain,'text',x))
	
def deleteSelectedArguments(*args):
	print("In procedure to delete selected arguments")
	selection = args[0]
	conn = args[1]
	grid = args[2]
	command = [args[3]]
	btn_edit = args[4]
	btn_sub = args[5]
	ret = DBConn.deleteArgDetails(selection,conn)
	if ret == 1:
		for children in grid.children:
			if children.id in selection:
				grid.remove_widget(children)
			if children.id in selection:
				selection.remove(children.id)
	
	
	if len(selection) == 1:
		btn_edit.disabled = False
		btn_sub.disabled = False
	elif len(selection) > 1:
		btn_edit.disabled = True
		btn_sub.disabled = False
	else:
		btn_edit.disabled = True
		btn_sub.disabled = True
		
def addArgument(*args):
	print("In Procedure to add arguments")
	dictOfCommands = args[0]
	selection = args[1]
	dbConn = args[2]
	commandID = args[3]
	popupAddArgument = createP1("Add argument Description below","Add Argument","",dictOfCommands,commandID,dbConn)
	popupAddArgument.open()

def refreshContents(*args):
	grid = args[0]
	grid.clear_widgets()
	conn = args[1]
	commandList = [args[2]]
	selection = args[3]
	btn_edit = args[4]
	btn_sub = args[5]
	conn.fetchArgumentsForSelectCommands(commandList)
	for eachArg in conn.dictOfArguments:
		string = "{arg}".format(arg=conn.dictOfArguments[eachArg])
		btn = myButton(text=string,id=str(eachArg))
		grid.add_widget(btn)
		btn.bind(on_press=Par(selectArg,btn,selection,btn_edit,btn_sub))
		
	if len(selection) == 1:
		btn_edit.disabled = False
		btn_sub.disabled = False
	elif len(selection) > 1:
		btn_edit.disabled = True
		btn_sub.disabled = False
	else:
		btn_edit.disabled = True
		btn_sub.disabled = True
		
	
def createP1(*args):
	stat = args[0]
	popupTitle = args[1]
	message = args[2]
	netText = stat + '\n' + message
	mainBox = BoxLayout(orientation='vertical',id="mainBoxID")
	label = Label(text=netText, color=(1,1,0,1),size_hint=(1,.15),id="labelID",multiline=True)
	innerButtonControlBox = BoxLayout(orientation='horizontal', size_hint=(1,.1),id="innerButtonControlBoxID")
	btn_ok = Button(text='Ok',background_color=(1,0,0,1),id="btn_okID")
	

	innerButtonControlBox.add_widget(btn_ok)
	mainBox.add_widget(label)
	
	if stat == 'Failure':
		err = args[3]
		label2 = Label(text=str(err.msg),multiline=True,color=(1,0,0,1),id="label2ID")
		mainBox.add_widget(label2)
		
	if popupTitle == 'Display Argument Details':
		selection = []
		dictOfArguments = args[3]
		dictOfCommands = args[4]
		dbConn = args[5]
		dictOfArgVal = args[6]
		command = args[7][0]
		print(command)
		#print(dictOfArgVal)
		gridlayout = GridLayout(cols=2,id="gridlayoutID")
		btn_refresh = Button(text='Refresh Content',font_size=12,background_color=(0,1,0,1))
		btn_add = Button(text='Add Argument',font_size=12,background_color=(0,1,0,1))
		btn_sub = Button(text='Delete Selected Arguments',font_size=12,background_color=(0,1,0,1))
		btn_sub.disabled = True
		box = BoxLayout(orientation='horizontal',size_hint=(1,.1))
		box.add_widget(btn_refresh)
		box.add_widget(btn_add)
		box.add_widget(btn_sub)
		mainBox.add_widget(gridlayout)
		mainBox.add_widget(box)
		btn_edit = Button(text='Edit',background_color=(1,0,0,1))
		btn_edit.bind(on_press=Par(editSelection))
		btn_add.bind(on_press=Par(addArgument,dictOfCommands,selection,dbConn,command))
		btn_sub.bind(on_press=Par(deleteSelectedArguments,selection,dbConn,gridlayout,command,btn_edit,btn_sub))
		btn_refresh.bind(on_press=Par(refreshContents,gridlayout,dbConn,command,selection,btn_edit,btn_sub))
		btn_edit.disabled = True
		innerButtonControlBox.add_widget(btn_edit)
		for eachArg in dictOfArguments:
			string = "{arg}".format(arg=args[3][eachArg])
			btn = myButton(text=string,id=str(eachArg))
			gridlayout.add_widget(btn)
			btn.bind(on_press=Par(selectArg,btn,selection,btn_edit,btn_sub))
		
	if popupTitle == 'Add Argument':
		dictOfCommands = args[3]
		commandList = args[4]
		dbConn = args[5]
		gridlayout = GridLayout(cols=2,id="gridlayoutID")
		label1 = Label(text="Argument Description: ",color=(1,0,0,1),id="label1ID")
		gridlayout.add_widget(label1)
		txtInpt = TextInput(id='textInputForArgumentID') #validation required for argument text
		gridlayout.add_widget(txtInpt)
		btn = Button(text="Click to import from another command",font_size=10,id="btnID",size_hint=(.75,1))
		gridlayout.add_widget(btn)
		btn_val = Button(text="Click to add values",font_size=10,id='valButtonID',size_hint=(.25,1))
		gridlayout.add_widget(btn_val)
		labelImport = Label(text="Import Tag: ",color=(1,0,0,1),id="labelImportID")
		txtInptImport = TextInput(id="textInputForImportTagID")
		txtInptImport.disabled = True
		gridlayout.add_widget(labelImport)
		gridlayout.add_widget(txtInptImport)
		mainBox.add_widget(gridlayout)
		btn_save = Button(text="Save to DB",background_color=(1,0,0,1),id="buttonSaveID")
		innerButtonControlBox.add_widget(btn_save)
		btn.bind(on_press=Par(displayCommands,dictOfCommands,btn,txtInptImport,btn_val))
		btn_val.bind(on_press=Par(addValues))
		btn_save.bind(on_press=Par(DBConn.processArgEntry,txtInpt,commandList,dbConn,txtInptImport,btn))
			
		
	if popupTitle == 'Commands':
		gridlayout = GridLayout(cols=3,id="gridIDPopUP")
		print(args[3])
		for eachCommand in args[3]:
			idString = str(eachCommand)
			btn_tmp = myButton(text=args[3][eachCommand], id=idString, background_color= (1,1,0,1))
			gridlayout.add_widget(btn_tmp)
			btn_tmp.bind(on_press=Par(disableOthers,gridlayout,idString))
		mainBox.add_widget(gridlayout)
		
		
	if popupTitle == 'Add Values':
		boxLayout  = BoxLayout(orientation='horizontal',size_hint=(1,.6))
		boxLayoutSmall = BoxLayout(orientation='vertical',size_hint=(.3,1))
		labelArg = Label(text="Argument Values:",font_size=8, color=(0,1,0,1))
		boxLayoutSmall.add_widget(labelArg)
		boxLayout.add_widget(boxLayoutSmall)
		gridlayout = GridLayout(cols=2,id="gridlayoutID",size_hint=(.7,1))
		boxLayout.add_widget(gridlayout)
		btn_plus = Button(text='+',font_size=12,background_color=(0,1,0,1))
		btn_minus = Button(text='-',font_size=12,background_color=(0,1,0,1))
		boxSmall = BoxLayout(orientation='horizontal',size_hint=(.25,1))
		boxSmall.add_widget(btn_plus)
		boxSmall.add_widget(btn_minus)
		btn_add = Button(text='Save Values',font_size=12,background_color=(0,1,0,1))
		btn_sub = Button(text='Delete Values',font_size=12,background_color=(0,1,0,1))
		btn_sub.disabled = True
		box = BoxLayout(orientation='horizontal',size_hint=(1,.1))
		box.add_widget(boxSmall)
		box.add_widget(btn_add)
		box.add_widget(btn_sub)
		mainBox.add_widget(boxLayout)
		mainBox.add_widget(box)
		btn_plus.bind(on_press=Par(addDetails,gridlayout))
	
	btn_cancel = Button(text="Cancel",background_color=(1,0,0,1),id="buttonCanID")
	
	innerButtonControlBox.add_widget(btn_cancel)
	mainBox.add_widget(innerButtonControlBox)

	popup1 = Popup(title=popupTitle, content=mainBox, size_hint=(None,None), size=(550,500), auto_dismiss=False,id="Popup1ID")
	btn_ok.bind(on_release=popup1.dismiss)
	btn_cancel.bind(on_release=popup1.dismiss)
	if popupTitle == 'Commands':
		btn_cancel.bind(on_press=Par(enableAll,gridlayout))
		return popup1, gridlayout
	elif popupTitle == 'Add Argument':
		btn_save.bind(on_release=popup1.dismiss)
		return popup1
	else:
		return popup1
	
class myButton(Button):
	background_color_normal = list([.5,.2,.2,1])
	background_color_down = list([0,1,0,1])

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