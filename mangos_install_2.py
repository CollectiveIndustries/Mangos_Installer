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
# CREDITS: William Baggett for color scheme, Levi Modl for Logo Idea,
#
##################################################################################################

## Global Settings ##
INSTALL_DIR = '/opt/ci_mangos3/'
SYS_USR = 'mangos'


## DO NOT CHANGE BELOW THIS LINE ##

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

## SCRIPT GLOBALS ##
_DEBUG_ = False
SERV_HOME = '/home/' + SYS_USR
CODE_BASE = SERV_HOME + '/SOURCE' #will be used to clone all the code and compile the software (can be removed after the install)
SQL_USR_INST = 'mangos-ci-usr.sql'
## _LOC_SQL_UPDATES_ = SERV_CODE + '/server/sql/updates/'

##################################### Function Definitions #####################################


## DEBUG FUNCTION ##
def debug(string,value):
	if _DEBUG_ is True:
		print "%s DEBUG: %s %s" % (TimeStamp(), string, value)
		

## reset cursor postion in terminal ##
def cur_pos(x_pos,y_pos,MSG,color):
	"""Function to set cursor position"""
	if not _DEBUG_:
		print "\033[%s;%sH\x1b[%sm %s \x1b[0m" % (y_pos,x_pos,color,MSG) #set cursor to X,Y pos and print MSG
	else:
		print "%s" % (MSG)

# CI MANGOS LOGO HERE
# Idea by Levi Modl
# adapted to work with Python by Andrew Malone
# color implimented 9-15-2014 sugested by William Baggett 
def logo():                                                                              ## PRINTS OUT WHITE BOARDER ##
	print "\x1b[0;92;40m                                                              \x1b[0;32;47m  \x1b[0m" #bright green on black no formatting
	print "\x1b[0;92;40m CCCCC       IIIIIIIII                                        \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC             III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC     ====    III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC     ====    III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC             III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40m CCCCC       IIIIIIIII     \x1b[0mhttp://ci-main.no-ip.org/          \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m                                                              \x1b[0;32;47m  \x1b[0m" ## MANGOS LOGO COLORING ##
	print "\x1b[0;91;44mMM   MM         NN   NN  GGGGG   OOOO   SSSSS                 \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM         NN   NN GGG GGG OO  OO SSS SSS                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMMM MMM         NNN  NN GGG GGG OO  OO SSS                    \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM M MM         NNNN NN GGG     OO  OO  SSS                   \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM M MM  AAAAA  NN NNNN GGG     OO  OO   SSS                  \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM M MM A   AAA NN  NNN GGGGGGG OO  OO    SSS                 \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM     AAA NN   NN GG  GGG OO  OO     SSS                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM AAAAAAA NN   NN GGG GGG OO  OO SSS SSS                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM AA  AAA NN   NN  GGGGGG  OOOO   SSSSS                 \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m        AA  AAA                                               \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m        AAAAAA                                                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m                           http://www.getmangos.co.uk/        \x1b[0;32;47m  \x1b[0m"
	print ""
	(width, height) = getTerminalSize()
	print "\x1b[0;32;47m" #White block border #
	for x in range(0,65):
		print "\033[%s;%sH " % (25,x)
	print "\x1b[0m"
# END LOGO

## Builds the Text based GUI ##
def reset_scrn():
	os.system('cls' if os.name == 'nt' else 'clear')
        logo()
	prt_dict(INSTALLER_SETTINGS,10)
	
## Returns a formatted Time Stamp ##
def TimeStamp():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

## host name of system ##
def HostName():
	hostname = subprocess.check_output(["uname", "-n"])
	if hostname[-1] == '\n':
		debug("HostName() []:",hostname[:-1])
		hostname = hostname[:-1]
	return hostname #return only the host name no New line

## CONSOLE SIZE ##
def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])


## setts a new value to the Settings List ##
def set_option(k,v,defualt):
	"""sets a new value for a KEY (k) passed to the function"""
	#width of console EX 157	
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
			## GIT CODE LOCATIONS ##
			"GIT_REPO_CI_SERVER":	CODE_BASE+"/server",
			"GIT_REPO_CI_DBS":	CODE_BASE+"/database",
			"GIT_REPO_CI_SD2":	CODE_BASE+"/server/src/bindings/ScriptDev2", ## SCRIPT DEV LIBARAY DESTINATION
			"GIT_REPO_CI_TOOLS":	CODE_BASE+"/tools",
			"GIT_REPO_CI_WEB":	CODE_BASE+"/web",			
			## FILE STRUCTURE ##
			"MANGOS_LOGS_DIR": 	"logs",# Path is relitave to the INSTALL_DIR
			"MANGOS_DATA_DIR":	"data" # Path is relitave to the INSTALL_DIR
#			"
			}

## print out the Settings List ##
def prt_dict(stuff,start):
	"""prints out key value pairs on seprate lines"""
	(width, height) = getTerminalSize()
	x_pos = width - 80
	y_pos = start
	print "\x1b[4;32;40m"
	print "\033[%s;%sH%s" % (start,x_pos,"-=/\=-    MaNGOS Install Options    -=/\=-")
	print "\x1b[0m"
	for k,v in stuff.items():
		y_pos += 1
		print "\033[%s;%sH     %s" % (y_pos,x_pos,k)
		print "\033[%s;%sH%s" % (y_pos,x_pos+26,v)
def UserName():
	return getpass.getuser()

## Clean a full directory path ##
def clean_dir(path):
	for file in os.listdir(path):
		file_path = os.path.join(path, file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)# Clean out files
				cur_pos(1,26,TimeStamp()+" Unlinking: "+file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)# delete folders recursively
				cur_pos(1,26,TimeStamp()+" Removing Directory Tree: "+file_path)
		except Exception, e:
			print e

## START OF MAIN PROGRAM ##
def main():
	reset_scrn()
	cur_pos(1,26,"Welcome to the MaNGOS installer.\nDurring this script we will figure out how you want your MaNGOS server set up","0;0;0")
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


	## BUILD PATH ##
	subprocess.call(shlex.split('sudo rm -Rf '+SERV_HOME))
	subprocess.call(shlex.split('sudo groupadd --system '+INSTALLER_SETTINGS["m_sys_usr"]))
	subprocess.call(shlex.split('sudo mkdir -p '+CODE_BASE))
	subprocess.call(shlex.split('sudo chown -R '+UserName()+':'+INSTALLER_SETTINGS["m_sys_usr"]+' '+CODE_BASE))## set perms for user to clone ##
	## Initilize Repository ##
	reset_scrn()
	cur_pos(1,28,"CLONING REPOSITORY TO "+INSTALLER_SETTINGS["GIT_REPO_CI_SERVER"],"1;31;40")
	git_server_handle = Repo.clone_from("https://github.com/CollectiveIndustries/server.git",INSTALLER_SETTINGS["GIT_REPO_CI_SERVER"])
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
	subprocess.call(shlex.split('sudo chown -R '+UserName()+':'+INSTALLER_SETTINGS["m_sys_usr"]+' '+CODE_BASE))## set the owner of the directory so we can leave ROOT
		
	## Configuration Files ##
	

	## DATABASE QUESTION ##
	
	## Print out settings for debug info ##
#	prt_dict(INSTALLER_SETTINGS,26)
#	print_format_table()		
if __name__ == '__main__':
    main()