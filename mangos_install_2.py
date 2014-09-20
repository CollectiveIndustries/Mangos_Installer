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
from subprocess import call
import datetime
import os 
import subprocess 
import shlex 
import getpass 
import time 
import urllib2 
import os.path
import glob
import CI_COLORS # COLOR CODES
import datetime
from git import * #for our git tools and bindings

import MySQLdb ## import the MySQLdb Connector API

## ManGOS install Library ##
from MaNGOS_core import settings ## we need our settings or this will fail
from MaNGOS_core import environment
from MaNGOS_core import gui


##################################### Function Definitions #####################################



## START OF MAIN PROGRAM ##
def main():
	## TODO rebuild Q + A section with a loop to dynamicly load values from the settings dictionary ##
	reset_scrn()
	cur_pos(1,26,"Welcome to the MaNGOS installer.\nDurring this script we will figure out how you want your MaNGOS server set up","0;0;0")
	raw_input("Press Enter to initilize installer....")
	reset_scrn()
	cur_pos(1,26,"Host name for account DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["REALM_DB_HOST"]+"\x1b[4;32;40m]?","4;32;40")
	set_option("REALM_DB_HOST",raw_input("REALM_DB_HOST: "),INSTALLER_SETTINGS["REALM_DB_HOST"])
	reset_scrn()
	cur_pos(1,26,"Port number for account DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["ACCOUNT_DB_PORT"]+"\x1b[4;32;40m]?","4;32;40")
	set_option("ACCOUNT_DB_PORT",raw_input("ACCOUNT_DB_PORT: "),INSTALLER_SETTINGS["ACCOUNT_DB_PORT"])
	reset_scrn()
        cur_pos(1,26,"Host name for world DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["M_DB_HOST"]+"\x1b[4;32;40m]?","4;32;40")
        set_option("M_DB_HOST",raw_input("M_DB_HOST: "),INSTALLER_SETTINGS["M_DB_HOST"])
	reset_scrn()
	cur_pos(1,26,"Port number for world DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["M_DB_PORT"]+"\x1b[4;32;40m]?","4;32;40")
	set_option("M_DB_PORT",raw_input("M_DB_PORT: "),INSTALLER_SETTINGS["M_DB_PORT"])
	reset_scrn()
        cur_pos(1,26,"MaNGOS version (1 vanilla - 5 MoP)[\x1b[1;31;40m"+INSTALLER_SETTINGS["SRV_VER"]+"\x1b[4;32;40m]?","4;32;40")
        set_option("SRV_VER",raw_input("SRV_VER: "),INSTALLER_SETTINGS["SRV_VER"])
	reset_scrn()
        cur_pos(1,26,"RealmID Number [\x1b[1;31;40m"+INSTALLER_SETTINGS["REALM_ID"]+"\x1b[4;32;40m]?","4;32;40")
        set_option("REALM_ID",raw_input("REAM_VER: "),INSTALLER_SETTINGS["REALM_ID"])
	reset_scrn()
	cur_pos(1,26,"Realm Name [\x1b[1;31;40m"+HostName()+"\x1b[4;32;40m]","4;32;40")
	set_option("REALM_NAME",raw_input("REALM_NAME: "),HostName())## use system host name for realm name by defualt
	reset_scrn()
	cur_pos(1,26,"New Account Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["ACCOUNT_DB"]+"\x1b[4;32;40m]","4;32;40")
	set_option("ACCOUNT_DB",raw_input("ACCOUNT_DB: "),INSTALLER_SETTINGS["ACCOUNT_DB"])
	reset_scrn()
        cur_pos(1,26,"New World Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["WORLD_DB"]+INSTALLER_SETTINGS["REALM_NAME"]+"\x1b[4;32;40m]","4;32;40")
        set_option("WORLD_DB",raw_input("WORLD_DB: "),INSTALLER_SETTINGS["WORLD_DB"]+INSTALLER_SETTINGS["REALM_NAME"])
	reset_scrn()
        cur_pos(1,26,"New ScriptDev2 Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["SCRIPTS_DB"]+INSTALLER_SETTINGS["REALM_NAME"]+"\x1b[4;32;40m]","4;32;40")
        set_option("SCRIPTS_DB",raw_input("SCRIPTS_DB: "),INSTALLER_SETTINGS["SCRIPTS_DB"]+INSTALLER_SETTINGS["REALM_NAME"])
	reset_scrn()
        cur_pos(1,26,"New Characters Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["CHAR_DB"]+INSTALLER_SETTINGS["REALM_NAME"]+"\x1b[4;32;40m]","4;32;40")
        set_option("CHAR_DB",raw_input("CHAR_DB: "),INSTALLER_SETTINGS["CHAR_DB"]+INSTALLER_SETTINGS["REALM_NAME"])
	reset_scrn()
	cur_pos(1,26,"New System User: [\x1b[1;31;40m"+INSTALLER_SETTINGS["MANGOS_USR"]+"\x1b[4;32;40m]","4;32;40")
        set_option("MANGOS_USR",raw_input("MANGOS_USR: "),INSTALLER_SETTINGS["MANGOS_USR"])
	reset_scrn()
        cur_pos(1,26,"\x1b[1;31;40m"+INSTALLER_SETTINGS["MANGOS_USR"]+"\x1b[4;32;40m System Password: [\x1b[1;31;40m"+INSTALLER_SETTINGS["MANGOS_PASS"]+"\x1b[4;32;40m]","4;32;40")
        set_option("MANGOS_PASS",raw_input("MANGOS_PASS: "),INSTALLER_SETTINGS["MANGOS_PASS"])

	## BUILD PATH ##
	subprocess.call(shlex.split('sudo rm -Rf '+SERV_HOME))
	subprocess.call(shlex.split('sudo groupadd --system '+INSTALLER_SETTINGS["MANGOS_USR"]))
	subprocess.call(shlex.split('sudo mkdir -p '+CODE_BASE))
	subprocess.call(shlex.split('sudo chown -R '+UserName()+':'+INSTALLER_SETTINGS["MANGOS_USR"]+' '+CODE_BASE))## set perms for user to clone ##
	## Initilize Repository ##
	reset_scrn()
	cur_pos(1,28,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_SERVER"],"1;31;40")
	git_serSRV_VER_handle = Repo.clone_from("https://github.com/CollectiveIndustries/serSRV_VER.git",INSTALLER_SETTINGS["GIT_REPO_CI_SERVER"])
	#reset_scrn()
	cur_pos(1,29,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_DBS"],"1;31;40")
	git_database_handle = Repo.clone_from("https://github.com/CollectiveIndustries/Mangos_world_database.git",INSTALLER_SETTINGS["GIT_REPO_CI_DBS"])
	#reset_scrn()
	cur_pos(1,30,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_SD2"],"1;31;40")
	git_maps_handle = Repo.clone_from("https://github.com/CollectiveIndustries/scripts.git",INSTALLER_SETTINGS["GIT_REPO_CI_SD2"])
	#reset_scrn()
	cur_pos(1,31,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_WEB"],"1;31;40")
	git_web_handle = Repo.clone_from("https://github.com/CollectiveIndustries/mangos-enhanced.git",INSTALLER_SETTINGS["GIT_REPO_CI_WEB"])
	#reset_scrn()
	cur_pos(1,32,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_TOOLS"],"1;31;40")
	git_tools_handle = Repo.clone_from("https://github.com/CollectiveIndustries/tools",INSTALLER_SETTINGS["GIT_REPO_CI_TOOLS"])
	
	## change owner of directories ##
	subprocess.call(shlex.split('sudo chown -R '+UserName()+':'+INSTALLER_SETTINGS["MANGOS_USR"]+' '+CODE_BASE))## set the owner of the directory so we can leave ROOT
		
	## Configuration Files ##
	

	## DATABASE QUESTION ##
	

if __name__ == '__main__':
	
	## Initilize the Settings Dictionary ##
	INSTALLER_SETTINGS = settings.BuildSettings(settings.INSTALLER_LST)
	
	## Enter Main Program ##
	main()
