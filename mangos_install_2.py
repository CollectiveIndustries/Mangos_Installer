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

_DEBUG_ = False


## INCLUDES ##
from git import * #for our git tools and bindings
import MySQLdb ## import the MySQLdb Connector API
import subprocess
import shlex

## ManGOS install Library ##
from MaNGOS_core import settings 		## we need our settings or this will fail
from MaNGOS_core import environment as env	## Environment API calls
from MaNGOS_core import gui			## Custom GUI tools


##################################### Function Definitions #####################################
def DefSettings(stuff):
	"""fucntion interacts with the user and defines all settings based on the dictionary we built"""
	for key in stuff.keys():
		gui.reset_scrn(stuff)
		gui.cur_pos(1,26,stuff[key][0],"4;32;40")## print out info ##
		if stuff[key][1] is 0: ## this is a user input feild
			stuff = settings.set_option(key,raw_input(key+"[\x1b[1;31;40m"+stuff[key][2]+"\x1b[0m]: "),stuff[key][2],stuff)## get input from user and place back into our settings



## START OF MAIN PROGRAM ##
def main():
	## TODO rebuild Q + A section with a loop to dynamicly load values from the settings dictionary ##
	gui.reset_scrn(INSTALLER_SETTINGS)
	gui.cur_pos(1,26,"Welcome to the MaNGOS installer.\nDurring this script we will figure out how you want your MaNGOS server set up","0;0;0")
	raw_input("Press Enter to initilize installer....")
	## BUILD OPTIONS WITH USER INPUT ##
	DefSettings(INSTALLER_SETTINGS)

	## BUILD PATH ##
	subprocess.call(shlex.split('sudo rm -Rf '+settings.SERV_HOME))
	subprocess.call(shlex.split('sudo groupadd --system '+INSTALLER_SETTINGS["MYSQL_MANGOS_USR"][2]))
	subprocess.call(shlex.split('sudo mkdir -p '+settings.CODE_BASE))
	subprocess.call(shlex.split('sudo chown -R '+env.UserName()+':'+INSTALLER_SETTINGS["MYSQL_MANGOS_USR"][2]+' '+settings.CODE_BASE))## set perms for user to clone ##
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
	subprocess.call(shlex.split('sudo chown -R '+env.UserName()+':'+INSTALLER_SETTINGS["MYSQL_MANGOS_USR"][2]+' '+settings.CODE_BASE))## set the owner of the directory so we can leave ROOT
		
	## Configuration Files ##
	

	## DATABASE QUESTION ##
	

if __name__ == '__main__':
	
	## Initilize the Settings Dictionary ##
	INSTALLER_SETTINGS = settings.BuildSettings(settings.INSTALLER_LST)
	
	## Enter Main Program ##
	main()
