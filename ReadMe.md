Software Package Testing Automation Framework 1.0
Author: Arko Basu
Organization: HGST Inc

Introduction

The application mountLocation is a generic 3 tier application that enables the user to test CLI based software packages on multiple systems. It is built using Python 3.4 and APIs like Kivy, and MysqlDataConnector.
The way this application works is, it has a GUI with which the user can access the framework and create new test suits, by creating software packages, adding their commands, corresponding arguments and their respective values. These GUI transaction ends up saving respective data sets in an already mapped RDBMS schema set where the tables are organized in a fashion to accommodate software packages details, along with commands, arguments, and values in a heirarchical manner.
The user can also create complex test suits with multiple argument sets for a single command. The entire information is stored in a database in form of mappings and are then used to generate scripts at desired location.
Once the scripts are built they can be fetched from sub/slave systems using a separate program which runs these scripts and logs the output of the script run into log files.

Installation

Requirements
	1. Python 3.3 and above - (Installed as default in all standard OS these days, or else, download from https://www.python.org/downloads/)
	2. Kivy - (Install and download from http://kivy.org/docs/gettingstarted/installation.html)
	3. MySQL Connector/Python - (Install OS Specific from https://dev.mysql.com/downloads/connector/python/2.0.html)
	4. Source code of the application framework found at http://sitrc.rochester.hgst.com/Arko.Basu/CompleteFramework or at //nserver.hgst.com/softwaretoolstest
	
After downloading the source code from the git repository or the nserver remote location, in order to run the framework GUI section you would need to run the program: appScript.py, and in order to run the script running section from remote/slave/sub systems you'd need to run the program: setup.py
In order for it to run successfully, you would need to have a all the other dependencies as mentioned above along with its sub dependencies as required for each of them as mentioned in their website.
If you're working on a Linux based machine the installation for Kivy and MySQL connector/python is fairly straight forward and simple. Please make sure you install the dependecies using python 3.3 and not anything less than that.
But if you're working on a Windows based machine then runnning the entire installation of all dependencies can be tiresome and erroneous. Hence you can alternately download the protable kivy package folder inside the nserver location, and run the entire framework using the bash script inside it. But in order for this to work you would need to install the mysql connector python package for the portable python setup in the zipped folder. For that download the zipped source code from the above mentioned website and extract the contents inside the folder $HOME\extractedLocation\Kivy-1.9.0-py3.4-win32-x64\Python34\Lib\site-packages. Once done you're good to go and run the GUI section of the framework.
Also note that the database IP address needs to be configured. That is you just need to change the host IP address in the database.py file to match the database that is hosting the current DB. Please contact Matthew Gusenius <Matthew.Gusenius@hgst.com> or Amy Spinler <Amy.Spinler@hgst.com> at SitLAB to know about the IP of the DB where the server is hosted.
You could also create your own Database schema with all the corresponding mappings and an already existing example dataset (that of HDM) using the database.sql file inside the source directory. But for that you'd need to install MYSQL server in a location of your own choice and the installation of which is beyond the scope of this document.



