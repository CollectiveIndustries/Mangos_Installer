#!/usr/bin/python

##################################################################################################
#
# Copyright (C) 2014 Collective Industries 
# 
# AUTHOR: Andrew Malone 
#  
# TITLE: Mangos Installer
#
# PURPOSE: Sets up the Mangos installation environment, configures databases, sets up realms
# also builds all the code and installs game maps
#
# CREDITS: William Baggett for color scheme, Levi Modl for Logo Idea, see the README for more
#
##################################################################################################

## Global Settings ##
INSTALL_DIR = '/opt/ci_mangos3/'
SYS_USR = 'mangos'


## DO NOT CHANGE BELOW THIS LINE ##



## INCLUDES ##
import imp
import subprocess
import shlex

## install includes that are not from the standard library ##
# for some reason or another these will install however this script AFTER there install still crashes but the second run will include the library
# this is a known bug

try:
    imp.find_module('git')
    from git import * #for our git tools and bindings
except ImportError:
    print 'Module `git` not found: [ \x1b[0;92;40mINSTALLING\x1b[0m ]'
    subprocess.call(shlex.split('sudo apt-get install python-setuptools'))
    subprocess.call(shlex.split('sudo easy_install GitPython')) ## not found lets not crash the script just fix the issue and keep going
    from git import * #for our git tools and bindings

try:
    imp.find_module('MySQLdb')
    import MySQLdb #for our git tools and bindings
except ImportError:
    print 'Module `MySQLdb` not found: [ \x1b[1;31;40mINSTALLING\x1b[0m ]'
    subprocess.call(shlex.split('sudo apt-get install build-essential python-dev libmysqlclient-dev python-pip'))
    subprocess.call(shlex.split('sudo pip install MySQL-python')) ## not found lets not crash the script just fix the issue and keep going
    import MySQLdb ## import the MySQLdb Connector API

## ManGOS install Library ##
#
# Provided by: Andrew Malone
#
# Purpose: Used to hold standard MaNGOS core functions for the installer and all of its settings
#
from MaNGOS_core import settings 		## we need our settings or this will fail
from MaNGOS_core import environment as env	## Environment API calls
from MaNGOS_core import gui			## Custom GUI tools
from MaNGOS_core import libdb			## database library for Mangos_installer

##################################### Function Definitions #####################################
##
## for key, value in sorted(myDict.items(), key=lambda e: e[1][2]):

def DefSettings(stuff):
	"""fucntion interacts with the user and defines all settings based on the dictionary we built"""
	for key,value in sorted(stuff.items(), key=lambda e: e[1][3]):##sort the dictionary OF lists based on 3rd entry
		gui.reset_scrn(stuff)
		gui.cur_pos(1,27,stuff[key][0],"4;32;40")## print out info ##
		if stuff[key][1] is 0: ## this is a user input feild
			stuff = settings.set_option(key,raw_input(key+"[\x1b[1;31;40m"+stuff[key][2]+"\x1b[0m]: "),stuff[key][2],stuff)## get input from user and place back into our settings
		else: ## this is just information so give the user some time to read it 
			gui.cur_pos(1,27,stuff[key][0]+": \x1b[1;31;40m"+stuff[key][2],"1;32;40")## GREEN with RED option
			raw_input("Press Enter to continue installation....")


## START OF MAIN PROGRAM ##
def main():
	## TODO rebuild Q + A section with a loop to dynamicly load values from the settings dictionary ##
	## dynamic Q + A section finished DefSettings(STUFF)
	gui.reset_scrn(INSTALLER_SETTINGS)
	gui.cur_pos(1,27,"Welcome to the MaNGOS installer.\nDurring this script we will figure out how you want your MaNGOS server set up","0;0;0")
	raw_input("Press Enter to initilize installer....")
	
	## BUILD OPTIONS WITH USER INPUT ##
	DefSettings(INSTALLER_SETTINGS) ## Interact with user to define MaNGOS Environment Settings ##

	## BUILD PATH ##
	subprocess.call(shlex.split('sudo rm -Rf '+settings.SERV_HOME))
	subprocess.call(shlex.split('sudo rm -Rf '+INSTALLER_SETTINGS["INSTALL_DIR"][2])) ## We end up recompiling the server and reconfiguring it during an install ##
	subprocess.call(shlex.split('sudo groupadd --system '+INSTALLER_SETTINGS["MANGOS_SYS_GROUP"][2])) ## it is ideal to run bolth services on there own group
	subprocess.call(shlex.split('sudo groupadd --system '+INSTALLER_SETTINGS["REALMD_SYS_GROUP"][2])) ## this is to stick with the *IX standard way of things
	subprocess.call(shlex.split('sudo mkdir -p '+settings.CODE_BASE))
	subprocess.call(shlex.split('sudo mkdir -p '+INSTALLER_SETTINGS["INSTALL_DIR"][2])) ## build the install directory and get it ready to go
	subprocess.call(shlex.split('sudo chown -R '+env.UserName()+':'+INSTALLER_SETTINGS["MANGOS_SYS_GROUP"][2]+' '+settings.CODE_BASE)) ## set perms for user to clone ##
	## Initilize Repository ##
	gui.reset_scrn(INSTALLER_SETTINGS)
	gui.cur_pos(1,28,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_SERVER"][2],"1;31;40")
	git_server_handle = Repo.clone_from("https://github.com/CollectiveIndustries/server.git",INSTALLER_SETTINGS["GIT_REPO_CI_SERVER"][2])
	#reset_scrn()
	gui.cur_pos(1,29,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_DBS"][2],"1;31;40")
	git_database_handle = Repo.clone_from("https://github.com/CollectiveIndustries/Mangos_world_database.git",INSTALLER_SETTINGS["GIT_REPO_CI_DBS"][2])
	#reset_scrn()
	gui.cur_pos(1,30,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_SD2"][2],"1;31;40")
	git_maps_handle = Repo.clone_from("https://github.com/CollectiveIndustries/scripts.git",INSTALLER_SETTINGS["GIT_REPO_CI_SD2"][2])
	#reset_scrn()
	gui.cur_pos(1,31,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_WEB"][2],"1;31;40")
	git_web_handle = Repo.clone_from("https://github.com/CollectiveIndustries/mangos-enhanced.git",INSTALLER_SETTINGS["GIT_REPO_CI_WEB"][2])
	#reset_scrn()
	gui.cur_pos(1,32,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_TOOLS"][2],"1;31;40")
	git_tools_handle = Repo.clone_from("https://github.com/CollectiveIndustries/tools",INSTALLER_SETTINGS["GIT_REPO_CI_TOOLS"][2])

	## change owner of directories ##
	subprocess.call(shlex.split('sudo chown -R '+env.UserName()+':'+INSTALLER_SETTINGS["MANGOS_SYS_GROUP"][2]+' '+settings.CODE_BASE))## set the owner of the directory so we can leave ROOT

	## start the MySQL Install ##
	gui.reset_scrn(INSTALLER_SETTINGS)
	_realm_db_ = MySQLdb.connect(host=INSTALLER_SETTINGS["REALM_DB_HOST"][2],
				     user=INSTALLER_SETTINGS["MYSQL_REALMD_ADMIN_USR"][2],
				     passwd=INSTALLER_SETTINGS["MYSQL_REALMD_ADMIN_PASS"][2])## pull the connection settings out and pass to the MySQL Connection
	_realm_db_cur_ = _realm_db_.cursor() ## set up our cursor so we can comunicate with the database
	_realm_db_cur_.execute("CREATE USER "+INSTALLER_SETTINGS["MYSQL_REALMD_USR"][2]+"@"+INSTALLER_SETTINGS["REALM_DB_HOST"][2]+" IDENTIFIED BY \'"+INSTALLER_SETTINGS["MYSQL_REALMD_PASS"][2]+"\';")## NO TRAILING ';'
	
	## Configuration Files ##


if __name__ == '__main__':

	## Initilize the Settings Dictionary ##
	INSTALLER_SETTINGS = settings.BuildSettings(settings.INSTALLER_LST)

	## Enter Main Program ##
	main()
