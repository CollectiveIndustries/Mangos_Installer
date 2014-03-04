#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for pulling Mangos off the GiHub Repos and starting the build process 
# and then install Collective Industries MaNGOS software
#
##################################################################################################


# configurable globals also can be set using the full install option these are defualt values
# TODO: write an user input section to set variables or have the option to use all defaults

INSTALL_DIR = '/opt/mangos3_ci_server' 
SYS_USR = 'mangos'

# DO NOT EDIT BELOW LINE
#-----------------------------------------------------------------------------------------------#

host_name = ''#will be set using uname and check_output
SYS_PASS = '' #will be set using RAW_INPUT 
SERV_CODE = '/home/' + SYS_USR + '/SOURCE/mangos3_ci_code' #will be used to clone all the code and compile the software (can be removed after the install)
SQL_USR_INST = 'mangos-ci-usr.sql'

# import all of our needed functions
from subprocess import call 
import os 
import subprocess 
import shlex 
import getpass 
import time 
import urllib2 
import os.path
import MySQLdb

##################################################################################################################
#
# Functions
#
##################################################################################################################

# MySQL execution
def mysqlcon (filename)
	# MySQL Connection
	MySQLConnection(user='root', password='ROOT_PASS')
	# Open and read the fie as a single buffer
	fd = open(filename, 'r')
	sqlFile = fd.read()
	fd.close()

	# all MySQL commands (split on ';')
	sqlCommands = sqlFile.split(';')
	
	# Execute every command from the input file
	for command in sqlCommands;
		# this will skip and report errors
		# For example, if the tables do not yet exist, this will skip over
 		# the DROP TABLE commands
		try:
			c.execute(command)
		except OperationalError, msg:
			print "Command skipped: ", msg

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
print " CCCCC       IIIIIIIII   http://ci-main.comule.com/"
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

print "We will now begin to process all dependancies required to build the MaNGOS server" 
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
os.makedirs(os.path.join(SERV_CODE, "mangos3_ci_server")) #main server bin directory
subprocess.call('clear') #clear the screen after update + install
print "Directory paths created for install and compile"
keep_s_dir = raw_input('Would you like to save source code? [n] ')
if keep_s_dir == 'n':
	print "Source code directory will be erased after full install is finished" #only remove /opt/SOURCE/mangos3_ci_code/*

subprocess.call(shlex.split('sudo git clone https://github.com/mangosthree/server.git '+SERV_CODE+'/server'))#will clone server code to working directory
subprocess.call(shlex.split('sudo git clone https://github.com/mangosthree/database.git '+SERV_CODE+'/database'))#will clone server code to working directory
subprocess.call(shlex.split('sudo git clone https://github.com/mangosthree/scripts.git '+SERV_CODE+'/scripts'))#will clone server code to working directory
subprocess.call(shlex.split('sudo git clone https://github.com/mangosthree/EventAI.git '+SERV_CODE+'/EventAI'))#will clone server code to working directory
subprocess.call(shlex.split('sudo git clone https://github.com/mangosthree/tools.git '+SERV_CODE+'/tools'))#will clone server code to working directory

# START compile and begin install
os.makedirs(os.path.join(SERV_CODE+"/server/", "objdir")) #main server bin directory
#change to our compile directory and run the compile
with cd(SERV_CODE+"/server/objdir"):
	subprocess.call(shlex.split('sudo cmake .. -DCMAKE_INSTALL_PREFIX='+INSTALL_DIR))
	subprocess.call(shlex.split('sudo make'))
	subprocess.call(shlex.split('sudo make install')) 


#------------------------------------------- MaNGOS-CI BataBase install

subprocess.call('clear') # clear screen and wait for user

#install questions
mangos_new_ci_usr = raw_input('Name of the MaNGOS mysql user you wish to use: ') #im having problems with this line here
mangos_new_ci_usr_pass = raw_input('Password for new user: ')
print "Before we can setup the new MaNGOS user we need to log into mysql as root or another administrators acount"
mysql_root_ci_usr = raw_input('MySQL ADMIN username: ')
mysql_root_ci_pass = raw_input('ADMIN password: ')

print "Almost ready to start installing the Database\'s We need a few more things and then we\'re ready"
WORLD_DATABASE = raw_input('New World Database name: [mangos] ')
if WORLD_DATABASE == '':
	WORLD_DATABASE = 'mangos'
CHAR_DATABASE = raw_input('New Character Database: [characters] ')
if CHAR_DATABASE == '':
	CHAR_DATABASE = 'characters'
CHAR_DATABASE = raw_input('New ScriptDev2 Database: [scriptdev2] ')
if CHAR_DATABASE == '':
	SCRDEV2_DATABASE = 'scriptdev2'
CHAR_DATABASE = raw_input('New Account Database: [account] ')
if CHAR_DATABASE == '':
	ACC_DATABASE = 'account'
CI_MANGOS_VER = raw_input('Which version of MaNGOS do you wish to use (1 vanilla - 5 MoP): [4] ')
if CI_MANGOS_VER == '':
	CI_MANGOS_VER = '4' #defualt cata

#TODO add in a "switch" for URL replacement for the CI-MANGOS code
#we need to tell the user we dont have any other version just yet
if CI_MANGOS_VER != '4':
	print "The version of MaNGOS you have chosen (%s) is not avalible at this time we are defualting to: CATA 4.3.4 (15595)"
	CI_MANGOS_VER = '4'


#------------------------------------------ DataBase Strings

#CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
ADD_MANGOS_CI_USR_MYSQL = ('CREATE USER '+
                           mangos_new_ci_usr+
                           '@localhost'+ #TODO make this configurable
                           'IDENTIFIED BY '+
                           mangos_new_ci_usr_pass)

#TODO create MySQL database
ROOT_PASS = raw_input('What is the root username password for MySQL: [password] ')
if ROOT_PASS == '':
	ROOT_PASS = 'password'


# TODO merge sh script with Python to bring up a unified installer for the CI databases
#'SERV_CODE'+make_full_db.sh


#TODO add SQL statement for granting permissions to user for databases 
#TODO setup databases before importing them from github

# DATABASE QUERY FORMAT STRING: INSERT INTO `user` (`Host`, `User`, `Password`, `Select_priv`, `Insert_priv`, `Update_priv`, `Delete_priv`, `Create_priv`, `Drop_priv`, `Reload_priv`, `Shutdown_priv`, `Process_priv`, `File_priv`, `Grant_priv`, `References_priv`, `Index_priv`, `Alter_priv`, `Show_db_priv`, `Super_priv`, `Create_tmp_table_priv`, `Lock_tables_priv`, `Execute_priv`, `Repl_slave_priv`, `Repl_client_priv`, `Create_view_priv`, `Show_view_priv`, `Create_routine_priv`, `Alter_routine_priv`, `Create_user_priv`, `Event_priv`, `Trigger_priv`, `Create_tablespace_priv`, `ssl_type`, `ssl_cipher`, `x509_issuer`, `x509_subject`, `max_questions`, `max_updates`, `max_connections`, `max_user_connections`, `plugin`, `authentication_string`) VALUES ('%', 'mangos-ci', '*27921E15B85D135E57090C99DB45DC24444A1798', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'Y', 'N', 'N', 'Y', 'Y', 'Y', 'Y', 'N', 'Y', 'Y', 'Y', 'N', 'N', 'Y', 'Y', 'Y', 'Y', 'N', 'Y', 'Y', 'Y', '', '', '', '', 0, 0, 0, 0, '', NULL);


#CREATE DATABASE `testdbname`
PERMS_MANGOS_CI_USR_MYSQL = ('CREATE DATABASE' +
			     '`' +
			     WORLD_DATABASE +
			     '`')

#open a new file for writing 
mangos_ci_sql_inst = open('/home/'+SYS_USR+'/mangos-ci-usr.sql','w')#open a temporary file for writing our config we will switch to root and move it later

# Realm name (using server hostname TODO ??? automatic name generator ??? )
hostname = subprocess.check_output(["uname", "-n"])
if hostname[-1] == '\n':
        hostname = hostname[:-1] # strip ONLY the new line at the end of the word
subprocess.call('clear')
print "Host Name found: %s\nBuilding database......" % (hostname)
time.sleep(4)

#------------------------------ MySQL File Write
mangos_ci_sql_inst.write(ADD_MANGOS_CI_USR_MYSQL)
#mangos_ci_sql_inst.write(CREATE_MANGOS_CI_DB_MYSQL)
#mangos_ci_sql_inst.write(CREATE_CHAR_CI_DB_MYSQL)
#mangos_ci_sql_inst.write(CREATE_ACCOUNT_CI_DB_MYSQL)
#mangos_ci_sql_inst.write(CREATE_REALMD_CI_DB_MYSQL)

#file has been written
mangos_ci_sql_inst.close()
print "SQL file for MaNGOS DB install has been written to your home directory:"

#TODO use the mysql < databse to load in the new settings we just created


#final clean up steps
if keep_s_dir == 'n':
	keep_s_dir_confirm = raw_input('/!\\ WARNING: this will erase ALL code for CI-MaNGOS/!\\ continue? [n] ')
	if keep_s_dir_confirm == 'y':
		print "Removing source code directory per user request"
		subprocess.call(shlex.split('sudo rm -Rf /home/mangos/SOURCE/mangos3_ci_code'))
