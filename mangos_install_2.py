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
#
#
##################################################################################################

## Global Settings ##
INSTALL_DIR = '/opt/ci_mangos3/'
SYS_USR = 'mangos'


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
import CI_COLORS
import datetime

## DO NOT CHANGE BELOW THIS LINE ##
_DEBUG_ = False
SERV_CODE = '/home/' + SYS_USR + '/SOURCE/mangos3_ci_code' #will be used to clone all the code and compile the software (can be removed after the install)
SQL_USR_INST = 'mangos-ci-usr.sql'
_LOC_SQL_UPDATES_ = SERV_CODE + '/server/sql/updates/'

## Function Definitions ##
def debug(string,value):
	if _DEBUG_ is True:
		print "%s DEBUG: %s %s" % (TimeStamp(), string, value)
		
def cur_pos(x_pos,y_pos,MSG,color):
	"""Function to set cursor position"""
	if not _DEBUG_:
		print "\033[%s;%sH\x1b[%sm %s \x1b[0m" % (y_pos,x_pos,color,MSG) #set cursor to X,Y pos and print MSG
	else:
		print "%s" % (MSG)

# CI MANGOS LOGO HERE
# Idea by Levi Modl
# adapted to work with Python by Andrew Malone
# color implimented 9-15-2014
def logo():
	print "\x1b[0;92;40m" #bright green on black no formatting
	print " CCCCC       IIIIIIIII"
	print "CCC CCC         III"
	print "CCC CCC         III"
	print "CCC             III"
	print "CCC     ====    III"
	print "CCC     ====    III"
	print "CCC             III"
	print "CCC CCC         III"
	print "CCC CCC         III"
	print " CCCCC       IIIIIIIII     \x1b[0mhttp://ci-main.no-ip.org/"
	print "\x1b[0;91;44m" ## MANGOS LOGO COLORING ##
	print "MM   MM         NN   NN  GGGGG   OOOO   SSSSS "
	print "MM   MM         NN   NN GGG GGG OO  OO SSS SSS"
	print "MMM MMM         NNN  NN GGG GGG OO  OO SSS    "
	print "MM M MM         NNNN NN GGG     OO  OO  SSS   "
	print "MM M MM  AAAAA  NN NNNN GGG     OO  OO   SSS  "
	print "MM M MM A   AAA NN  NNN GGGGGGG OO  OO    SSS "
	print "MM   MM     AAA NN   NN GG  GGG OO  OO     SSS"
	print "MM   MM AAAAAAA NN   NN GGG GGG OO  OO SSS SSS"
	print "MM   MM AA  AAA NN   NN  GGGGGG  OOOO   SSSSS "
	print "        AA  AAA                               "
	print "        AAAAAA                                "
	print "\x1b[0m                            http://www.getmangos.co.uk/"
	print ""
# END LOGO
def reset_scrn():
	os.system('cls' if os.name == 'nt' else 'clear')
        logo()
	
def TimeStamp():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

def HostName():
	hostname = subprocess.check_output(["uname", "-n"])
	if hostname[-1] == '\n':
		debug("HostName() []:",hostname[:-1])
		hostname = hostname[:-1]
	return hostname #return only the host name no New line

def set_option(k,v,defualt):
	"""sets a new value for a KEY (k) passed to the function"""
	for key in INSTALLER_SETTINGS.keys():
        	if key == k:
			if v == '':
				INSTALLER_SETTINGS[key] = defualt
			else:
	            		INSTALLER_SETTINGS[key] = v

##### settings Dictionary #####
INSTALLER_SETTINGS = {	"realm_name": 		"",
			"r_db_host": 		"localhost",
			"r_db_port":		"3306",
			"m_db_host": 		"localhost",
			"m_db_port": 		"3306",
			"m_sys_usr": 		SYS_USR,
			"m_sys_pass":		"",#this has to be passed to the configuration scripts
			"w_db": 		"world-",
			"c_db":         	"characters-",
			"sd2_db":       	"scriptdev2-",
			"a_db":         	"realmd-account",
			"ver":			"4",
			"rid":			"1", # default realm 1
			"install_path":		INSTALL_DIR,
			## DATABASE USERS AND PASSWORDS ##
			"mysql_root_ci_usr":	"root",
			"mysql_root_ci_pass":	"",
			
			## FILE STRUCTURE ##
			"MANGOS_LOGS_DIR": 	"logs",# Path is relitave to the INSTALL_DIR
			"MANGOS_DATA_DIR":	"data" # Path is relitave to the INSTALL_DIR
#			"
			}

def prt_dict(stuff):
	"""prints out key value pairs on seprate lines"""
	for k,v in stuff.items():
		print k,v

## COLOR TABLES ##
def print_format_table():
    """prints table of formatted text format options"""
    for style in xrange(8):
        for fg in xrange(30,38):
            s1 = ''
            for bg in xrange(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print s1
        print '\n'


## START OF MAIN PROGRAM ##
def main():
	reset_scrn()
	cur_pos(1,26,"Welcome to the MaNGOS installer durring this script we will figure out how you want your MaNGOS server set up","0;0;0")
	raw_input("Press Enter to initilize installer....")
	reset_scrn()
	cur_pos(1,26,"Host name for account DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["r_db_host"]+"\x1b[4;32;40m]?","4;32;40")
	set_option("r_db_host",raw_input("HOST NAME: "),INSTALLER_SETTINGS["r_db_host"])
	reset_scrn()
	cur_pos(1,26,"Port number for account DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["r_db_port"]+"\x1b[4;32;40m]?","4;32;40")
	set_option("r_db_port",raw_input("PORT NUMBER: "),INSTALLER_SETTINGS["r_db_port"])
	reset_scrn()
        cur_pos(1,26,"Host name for world DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["m_db_host"]+"\x1b[4;32;40m]?","4;32;40")
        set_option("m_db_host",raw_input("HOST NAME: "),INSTALLER_SETTINGS["m_db_host"])
	reset_scrn()
	cur_pos(1,26,"Port number for world DB [\x1b[1;31;40m"+INSTALLER_SETTINGS["m_db_port"]+"\x1b[4;32;40m]?","4;32;40")
	set_option("m_db_port",raw_input("PORT NUMBER: "),INSTALLER_SETTINGS["m_db_port"])
	reset_scrn()
        cur_pos(1,26,"MaNGOS version (1 vanilla - 5 MoP)[\x1b[1;31;40m"+INSTALLER_SETTINGS["ver"]+"\x1b[4;32;40m]?","4;32;40")
        set_option("ver",raw_input("VER: "),INSTALLER_SETTINGS["ver"])
	reset_scrn()
        cur_pos(1,26,"RealmID Number [\x1b[1;31;40m"+INSTALLER_SETTINGS["rid"]+"\x1b[4;32;40m]?","4;32;40")
        set_option("rid",raw_input("RID: "),INSTALLER_SETTINGS["rid"])
	reset_scrn()
	cur_pos(1,26,"Realm Name [\x1b[1;31;40m"+HostName()+"\x1b[4;32;40m]","4;32;40")
	set_option("realm_name",raw_input("REALM: "),HostName())## use system host name for realm name by defualt
	reset_scrn()
	cur_pos(1,26,"New Account Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["a_db"]+"\x1b[4;32;40m]","4;32;40")
	set_option("a_db",raw_input("ACCOUNT DB: "),INSTALLER_SETTINGS["a_db"])
	reset_scrn()
        cur_pos(1,26,"New World Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["w_db"]+INSTALLER_SETTINGS["realm_name"]+"\x1b[4;32;40m]","4;32;40")
        set_option("w_db",raw_input("WORLD DB: "),INSTALLER_SETTINGS["w_db"]+INSTALLER_SETTINGS["realm_name"])
	reset_scrn()
        cur_pos(1,26,"New ScriptDev2 Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["sd2_db"]+INSTALLER_SETTINGS["realm_name"]+"\x1b[4;32;40m]","4;32;40")
        set_option("sd2_db",raw_input("SCRIPTS DB: "),INSTALLER_SETTINGS["sd2_db"]+INSTALLER_SETTINGS["realm_name"])
	reset_scrn()
        cur_pos(1,26,"New Characters Database: [\x1b[1;31;40m"+INSTALLER_SETTINGS["c_db"]+INSTALLER_SETTINGS["realm_name"]+"\x1b[4;32;40m]","4;32;40")
        set_option("c_db",raw_input("CHAR DB: "),INSTALLER_SETTINGS["c_db"]+INSTALLER_SETTINGS["realm_name"])
	reset_scrn()
	cur_pos(1,26,"New System User: [\x1b[1;31;40m"+INSTALLER_SETTINGS["m_sys_usr"]+"\x1b[4;32;40m]","4;32;40")
        set_option("m_sys_usr",raw_input("USER NAME: "),INSTALLER_SETTINGS["m_sys_usr"])
	reset_scrn()
        cur_pos(1,26,"\x1b[1;31;40m"+INSTALLER_SETTINGS["m_sys_usr"]+"\x1b[4;32;40m System Password: [\x1b[1;31;40m"+INSTALLER_SETTINGS["m_sys_pass"]+"\x1b[4;32;40m]","4;32;40")
        set_option("m_sys_pass",raw_input("PASSWORD: "),INSTALLER_SETTINGS["m_sys_pass"])
	
	## Configuration Files ##
	

	## DATABASE QUESTION ##
	
	## Print out settings for debug info ##
	prt_dict(INSTALLER_SETTINGS)
#	print_format_table()		
if __name__ == '__main__':
    main()
