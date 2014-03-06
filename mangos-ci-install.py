#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for pulling Mangos off the GiHub Repos and starting the build process 
# and then install Collective Industries MaNGOS software
#
##################################################################################################

# configurable globals also can be set using the full install option these are defualt values
#TODO: write an user input section to set variables or have the option to use all defaults
#TODO add in a system user creation section

INSTALL_DIR = '/opt/mangos3_ci_server/'
SYS_USR = 'mangos'

# DO NOT EDIT BELOW LINE
#-----------------------------------------------------------------------------------------------#

host_name = ''#will be set using uname and check_output
SYS_PASS = '' #will be set using RAW_INPUT 
SERV_CODE = '/home/' + SYS_USR + '/SOURCE/mangos3_ci_code' #will be used to clone all the code and compile the software (can be removed after the install)
SQL_USR_INST = 'mangos-ci-usr.sql'
_LOC_SQL_UPDATES_ = SERV_CODE + '/server/sql/updates/'
# import all of our needed functions
from subprocess import call 
import os 
import subprocess 
import shlex 
import getpass 
import time 
import urllib2 
import os.path
import glob

##################################################################################################################
#
# Functions
#
##################################################################################################################

# Collective Industries mysql call
def mysql_call(usr, psw, host, db, sql):
	"""Function for Adding sql files to MySQL Host"""
	os.system("mysql -u " + usr + " -p" + psw + " -h " + host + ' ' + db + "  < " + sql )
	
# mysql_call()

# Collective Industries git + compile functions
# clone https://github.com/mangosthree/EventAI.git '+SERV_CODE+'/EventAI'))
def git_api(command, args):
	"""Function for handling git commands"""
	#subprocess.call(shlex.split('sudo git '+command+' '+args)

# git_api()
##############################################################################################################################
#
#
# change directory class provided by http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
#
#
##############################################################################################################################

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)



##############################################################################################################################
#
#
# backport for ubuntu 10 (check_output was introduced in python 2.7)
#
#
##############################################################################################################################
if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

# SCRIPT ENTRY POINT
subprocess.call('clear') 
print "Welcome: " + getpass.getuser() 

if getpass.getuser() == 'root':
	print "/!\\ WARNING: script is being run as root /!\\\ndurring this script we will change to root as needed so system files do not get messed up durrning this install procedure"
	override = raw_input('override root security locks-outs? [n] ')
	if override == '':
		override = 'n'
	if override == 'n':
		print "Root Security Lockout: ENABLED\nthis script will now terminate"
		exit(1)#exit code 1 (debug info for calling scripts or for user need documentation in readme on exit codes)


subprocess.call(shlex.split('clear')) #clear the screen

# CI MANGOS LOGO HERE
# Idea by Levi Modl
# adapted to work with Python by Andrew Malone
print ""
print " CCCCC       IIIIIIIII"
print "CCC CCC         III"
print "CCC CCC         III"
print "CCC             III"
print "CCC     ====    III"
print "CCC     ====    III"
print "CCC             III"
print "CCC CCC         III"
print "CCC CCC         III"
print " CCCCC       IIIIIIIII   http://ci-main.no-ip.org/"
print ""
print "MM   MM         NN   NN  GGGGG   OOOO   SSSSS"
print "MM   MM         NN   NN GGG GGG OO  OO SSS SSS"
print "MMM MMM         NNN  NN GGG GGG OO  OO SSS"
print "MM M MM         NNNN NN GGG     OO  OO  SSS"
print "MM M MM  AAAAA  NN NNNN GGG     OO  OO   SSS"
print "MM M MM A   AAA NN  NNN GGGGGGG OO  OO    SSS"
print "MM   MM     AAA NN   NN GG  GGG OO  OO     SSS"
print "MM   MM AAAAAAA NN   NN GGG GGG OO  OO SSS SSS"
print "MM   MM AA  AAA NN   NN  GGGGGG  OOOO   SSSSS"
print "        AA  AAA"
print "        AAAAAA           http://www.getmangos.co.uk/"
print ""

# END LOGO

print "We will now begin to process all dependencies required to build the MaNGOS server" 
print "Running Update as user: " 
subprocess.call(shlex.split('sudo id -nu')) 
subprocess.call(shlex.split('sudo apt-get update -q --force-yes'))
subprocess.call(shlex.split('sudo apt-get dist-upgrade -q --force-yes'))
# END of system UPDATE

subprocess.call(shlex.split('clear'))
subprocess.call(shlex.split('sudo apt-get install -q --force-yes build-essential gcc g++ automake git-core autoconf make patch libmysql++-dev mysql-server libtool libssl-dev grep binutils zlibc libc6 libbz2-dev cmake'))
# END Preparation

#make our code directory
os.makedirs(os.path.join(SERV_CODE, "SOURCE", "mangos3_ci_code")) #main code directory
subprocess.call('clear') #clear the screen after update + install
print "Directory paths created for install and compile"
keep_s_dir = raw_input('Would you like to save source code? [n] ')
if keep_s_dir == 'n':
	print "Source code directory will be erased after full install is finished" #only remove /opt/SOURCE/mangos3_ci_code/*

#TODO add a commit log viewer (git log) option after each clone request
	
#TODO SWAP out urls for CI github repo AFTER code clean up and repo creation
git_api("clone", 'https://github.com/mangosthree/server.git '+SERV_CODE+'/server')
git_api("clone", 'https://github.com/mangosthree/database.git '+SERV_CODE+'/database')

#Clone ScriptDev2  - execute from within src/bindings directory
print "Chaging Directory to: "+SERV_CODE+"/server/src/bindings"
with cd(SERV_CODE+"/server/src/bindings"):
	git_api("clone", 'https://github.com/mangosthree/scripts.git ./ScriptDev2')
git_api("clone", 'https://github.com/mangosthree/EventAI.git '+SERV_CODE+'/EventAI')
git_api("clone", 'https://github.com/mangosthree/tools.git '+SERV_CODE+'/tools')

# START compile and begin install
os.makedirs(os.path.join(SERV_CODE+"/server/", "objdir")) #main server bin directory
#change to our compile directory and run the compile
with cd(SERV_CODE+"/server/objdir"):
	#subprocess.call(shlex.split('sudo cmake .. -DCMAKE_INSTALL_PREFIX='+INSTALL_DIR+' -DINCLUDE_BINDINGS_DIR=ScriptDev2'))
	#subprocess.call(shlex.split('sudo make'))
	#subprocess.call(shlex.split('sudo make install')) 


#------------------------------------------- MaNGOS-CI Bata Base install

subprocess.call('clear') # clear screen and wait for user

#generated Install Answers

# Realm name
CI_REALM_NAME = subprocess.check_output(["uname", "-n"])
if CI_REALM_NAME[-1] == '\n':
        CI_REALM_NAME = CI_REALM_NAME[:-1] # strip ONLY the new line at the end of the word
#install questions
	#Realm Name
CI_IN_REALM_NAME = raw_input('Realm Name: [' + CI_REALM_NAME +'] ')
if CI_IN_REALM_NAME == '':
	CI_IN_REALM_NAME = CI_REALM_NAME #blank input default set to hostname
	#Realmd DB hostname
CI_ACCOUNT_DB = raw_input('Hostname for ACCOUNT database (realmd): [localhost] ')
if CI_ACCOUNT_DB == '':
	CI_ACCOUNT_DB = 'localhost'
	#Mangos DB hostname
CI_MANGOS_DB = raw_input('Hostname for MANGOS database (mangosd): [localhost] ')
if CI_MANGOS_DB == '':
	CI_MANGOS_DB = 'localhost'
	#MANGOS_PORT
CI_MANGOS_DB_PORT = raw_input('Port number for MySQL Server on MaNGOS_DB (' + CI_MANGOS_DB + '): [3306] ')
if CI_MANGOS_DB_PORT == '':
	CI_MANGOS_DB_PORT = '3306'
	#realm port number
CI_REALM_DB_PORT = raw_input('Port number for MySQL Server on Realm_DB (' + CI_ACCOUNT_DB + '): [3306] ')
if CI_REALM_DB_PORT == '':
	CI_REALM_DB_PORT = '3306'
	#USR and password for NEW MANGOS USER
CI_MANGOS_USR = raw_input('Name of the MaNGOS mysql user you wish to use: ') 
CI_MANGOS_USR_PASS = raw_input('Password for new user: ')

print "Before we can set-up the new MaNGOS user we need to log into mysql as root or another administrators account"
mysql_root_ci_usr = raw_input('MySQL ADMIN username: ')
mysql_root_ci_pass = raw_input('ADMIN password: ')

print "Almost ready to start installing the Database\'s We need a few more things and then we\'re ready"

	# WORLD DB Questions
WORLD_DATABASE = raw_input('New World Database name: [mangos-' + CI_IN_REALM_NAME + '] ')
if WORLD_DATABASE == '':
	WORLD_DATABASE = 'mangos-'+CI_IN_REALM_NAME

	# CHAR db questions
CHAR_DATABASE = raw_input('New Character Database: [characters-' + CI_IN_REALM_NAME + '] ')
if CHAR_DATABASE == '':
	CHAR_DATABASE = 'characters-'+CI_IN_REALM_NAME

	# ScriptDev2	
SCRDEV2_DATABASE = raw_input('New ScriptDev2 Database: [scriptdev2-' + CI_IN_REALM_NAME + '] ')
if SCRDEV2_DATABASE == '':
	SCRDEV2_DATABASE = 'scriptdev2-'+CI_IN_REALM_NAME

	# Account 
ACC_DATABASE = raw_input('New Account Database: [realmd-account] ')
if ACC_DATABASE == '':
	ACC_DATABASE = 'realmd-account'

	# Mangos Realm Ver
CI_MANGOS_VER = raw_input('Which version of MaNGOS do you wish to use (1 vanilla - 5 MoP): [4] ')
if CI_MANGOS_VER == '':
	CI_MANGOS_VER = '4' #default cata

#TODO add in a "switch" for URL replacement for the CI-MANGOS code
#we need to tell the user we dont have any other version just yet
if CI_MANGOS_VER != '4':
	print "The version of MaNGOS you have chosen (%s) is not available at this time we are defaulting to: CATA 4.3.4 (15595)" %(CI_MANGOS_VER)
	CI_MANGOS_VER = '4'

## MaNGOS Configuration Questions for the realmd.conf and the mangosd.conf
# Config directory INSTALL_DIR + '/etc'


	# Log directory for mangos to use
CI_MANGOS_LOGS_DIR = raw_input('Log directory to use: [../logs] ')
if CI_MANGOS_LOGS_DIR == '':
	CI_MANGOS_LOGS_DIR = '../logs'

		# Data directory for mangos to use
CI_MANGOS_DATA_DIR = raw_input('data directory for maps: [../data] ')
if CI_MANGOS_DATA_DIR == '':
	CI_MANGOS_DATA_DIR = '../data'

	# RealmID 
print "Please enter the Realm ID below (if first realm installed use default)"
CI_MANGOS_REALM_ID = raw_input('RealmID: [1] ')
if CI_MANGOS_REALM_ID == '':
	CI_MANGOS_REALM_ID = '1'	
# TODO open file for configuration of the realmd and mangosd configs and get them ready to place in the config dir

#------------------------------------------ DataBase Strings
mangos_ci_sql_inst = open('/home/'+SYS_USR+'/mangos-ci-usr.sql','w')#open a temporary file for writing our config we will switch to root and move it later

### TODO change all DB strings to DROP IF EXIST then CREATE

#CREATE DATABASE `mangos` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
ADD_MANGOS_MYSQL = ('CREATE DATABASE `' + WORLD_DATABASE + '` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

#CREATE DATABASE `characters` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
ADD_MANGOS_MYSQL = ('CREATE DATABASE `' + CHAR_DATABASE + '` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

#CREATE DATABASE `realmd` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
ADD_MANGOS_MYSQL = ('CREATE DATABASE `' + ACC_DATABASE + '` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

#CREATE USER 'mangos'@'localhost' IDENTIFIED BY 'mangos';
ADD_MANGOS_MYSQL = ('CREATE USER '+ CI_MANGOS_USR + '@localhost ' + 'IDENTIFIED BY ' + CI_MANGOS_USR_PASS+';\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

#GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `mangos`.* TO 'mangos'@'localhost';
ADD_MANGOS_MYSQL = ('GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `'+WORLD_DATABASE+'`.* TO '+ CI_MANGOS_USR + '@localhost;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

#GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `characters`.* TO 'mangos'@'localhost';
ADD_MANGOS_MYSQL = ('GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `'+CHAR_DATABASE+'`.* TO '+ CI_MANGOS_USR + '@localhost;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

#GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `realmd`.* TO 'mangos'@'localhost';
ADD_MANGOS_MYSQL = ('GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `'+ACC_DATABASE+'`.* TO '+ CI_MANGOS_USR + '@localhost;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

#finalize the SQL file
mangos_ci_sql_inst.close()
print "SQL file for MaNGOS DB install has been written to your home directory: ["+'/home/'+SYS_USR+'/mangos-ci-usr.sql'+"]"

# run the upload
MYSQL_FILE_LOC = '/home/'+SYS_USR+'/mangos-ci-usr.sql'
#TODO get MySQL syntax for port number 
#edit -h for configurable host by DB NAME (realmd and mangosd) 
#IDEA set up host/port for each database (could be usefull in a multi server platform) (ENTERPRISE INSTALLER)

# DEPRECIATED os.system("mysql -u " + mysql_root_ci_usr + " -p" + mysql_root_ci_pass + " -h localhost" + " < " + MYSQL_FILE_LOC )#TODO add in -h CONFIG OPTION for REMOTE upload
mysql_call(mysql_root_ci_usr, mysql_root_ci_pass, 'localhost', ' ', MYSQL_FILE_LOC) #import user generated sql

#install WORLD DB
full_db = glob.glob(SERV_CODE + '/database/full_db/*.sql')
full_db = sorted(full_db)
print "Starting Patching Process"
print "User and Databases have been created now running MySQL installer for World Content"
#full_db = SERV_CODE + '/database/full_db/*.sql'
for sql in full_db:
	print "Adding: " + sql + " ---> " + WORLD_DATABASE
	mysql_call(mysql_root_ci_usr, mysql_root_ci_pass, 'localhost', WORLD_DATABASE, sql)#no host config set up yet 
	# DEPRECIATED os.system("mysql -u " + mysql_root_ci_usr + " -p" + mysql_root_ci_pass + " -h localhost " + WORLD_DATABASE + "  < " + sql )#TODO add in -h CONFIG OPTION for REMOTE upload

#Install EventAI
full_db = glob.glob(SERV_CODE + '/EventAI/*.sql')
full_db = sorted(full_db)
print "Now loading EventAI DataBase"
#full_db = SERV_CODE + '/EventAI/*.sql'
for sql in full_db:
	print "Adding: " + sql + " ---> " + WORLD_DATABASE
	mysql_call(mysql_root_ci_usr, mysql_root_ci_pass, 'localhost', WORLD_DATABASE, sql)#no host config set up yet
	# DEPRECIATED os.system("mysql -u " + mysql_root_ci_usr + " -p" + mysql_root_ci_pass + " -h localhost " + WORLD_DATABASE + "  < " + sql )#TODO add in -h CONFIG OPTION for REMOTE upload

#Install SCRDEV2_DATABASE
#Execute `sql\scriptdev2_create_database.sql` ## check file and make sure it matches installer options ##
#Execute `sql\scriptdev2_create_structure.sql` on SCRDEV2_DATABASE
#Add content to ScriptDev2-Database::
#Execute `sql\scriptdev2_script_full.sql` on SCRDEV2_DATABASE
#Update ScriptNames::
#Execute `sql\mangos_scriptname_full.sql` on WORLD_DATABASE	

#Data Base Update
patches = glob.glob(_LOC_SQL_UPDATES_ + '*.sql')
patches = sorted(patches)#sort the patches to upload in correct order
print "Starting Patching Process"
_DB_ = ''

for x in patches: #set up a loop to run through the current working directory
  print "Patching File: " + x #tell user what file is being added to the Database
  db = x.split("_")[2].replace('.sql', '')#this is for the Mangos FileName structure we have to sort them and find the database names
  if db == 'characters':
  	_DB_  = CHAR_DATABASE
  if db == 'realmd':
        _DB_ = ACC_DATABASE
  if db == 'mangos':
        _DB_ = WORLD_DATABASE  #block was for determining the database from the file name and the users input
  mysql_call(mysql_root_ci_usr, mysql_root_ci_pass, 'localhost', _DB_, x)#no host config set up yet

#file handles for Realmd, Mangosd, ScriptDev2 Configuration settings
#FILE_REALMD_CONF = open('/home/'+SYS_USR+'/realmd.conf','w')
#FILE_MANGOSD_CONF = open('/home/'+SYS_USR+'/mangosd.conf','w')
#FILE_SCRIPTDEV2_CONF = open('/home/'+SYS_USR+'/scriptdev2.conf','w')

# File Formatted Strings
##realmd.conf
# LoginDatabaseInfo = "HOST;PORT;USR;PASSWORD;DATABASE"
# LogsDir = "../logs"
# WrongPass.MaxCount = 0 
# WrongPass.BanTime = 600
# WrongPass.BanType = 0
# BindIP = "0.0.0.0"

##mangosd.conf
# RealmID = 1
# DataDir = "../data"
# LogsDir = "../logs"
# LoginDatabaseInfo = "HOST;PORT;USR;PASSWORD;DATABASE"
# WorldDatabaseInfo = "HOST;PORT;USR;PASSWORD;DATABASE"
# CharacterDatabaseInfo = "127.0.0.1;3306;mangos;mangos;characters"
# BindIP = "0.0.0.0"

# ADD Map_data to server
git_api("clone", 'https://github.com/CollectiveIndustries/server-maps.git '+INSTALL_DIR+CI_MANGOS_DATA_DIR)

#TODO add rc.local script section
# add lines to a file for running the mangosd and realmd services
# see local CI_START file for line references

#final clean up steps
if keep_s_dir == 'n':
	keep_s_dir_confirm = raw_input('/!\\ WARNING: this will erase ALL code for CI-MaNGOS/!\\ continue? [n] ')
	if keep_s_dir_confirm == 'y':
		print "Removing source code directory per user request"
		subprocess.call(shlex.split('sudo rm -Rf /home/mangos/SOURCE/mangos3_ci_code'))
