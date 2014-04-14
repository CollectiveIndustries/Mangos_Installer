#!/usr/bin/python

##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for pulling Mangos off the GiHub Repos and starting the build process 
# and then install Collective Industries MaNGOS software
#
##################################################################################################

# Import all of our needed functions
from subprocess import call
import os
import subprocess
import shlex
import getpass
import time
import urllib2
import glob
import npyscreen

# Variables
CI_REALM_NAME = '' # Realm Name

########################################
#
#  Collective Industries Main Menu
#
########################################
class MangosInstall(npyscreen.NPSApp):
    def main(self):
        
        global CI_REALM_NAME
        
        MIMenu = npyscreen.Form(name = 'Collective Industries MaNGOS Installer',) # Creates the Form Menu    
        CI_REALM_NAME = MIMenu.add(npyscreen.TitleText, name = 'Realm Name:', value = subprocess.check_output(["uname", "-n"]) # Realm Name
        
        MIMenu.edit() # This lets the user play with the Form
        

App = MangosInstall()
App.run()
