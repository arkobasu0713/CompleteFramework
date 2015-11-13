#Author: Arko Basu [HGST Inc.]
#Date: 10/26/2015
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
from screenClasses import *

Builder.load_file("appScript2.kv")
class AutomatedFrameworkForSoftwareTesting(App):
	def build(self):
		self.mapDriveAt = ''
		sm.add_widget(WelcomeScreen(name='WelcomeScreen'))
		sm.add_widget(ApplicationControlScreen(name='ApplicationConsole'))
		sm.add_widget(DisplayResultsScreen(name='DisplayResultsScreen'))
		sm.add_widget(CreateScreen(name='Create'))
		sm.add_widget(CreateCommandScreen(name='CreateCommandScreen'))
		sm.add_widget(CreateNewTestSuitScreen(name='CreateNewTestSuitScreen'))
		sm.add_widget(EditTestSuitScreen(name='EditTestSuitScreen'))
		return sm

	def mapDrive(self):
		self.mapDriveAt = UTIL.mappingNetworkDrive()
		if mapDriveAt != '':
			print("It has been mapped at: " + mapDriveAt)
	
if __name__ == '__main__':
	app = AutomatedFrameworkForSoftwareTesting()
	app.run()


