#!/usr/bin/python

##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for pulling Mangos off the GiHub Repos and starting the build process 
# and then install Collective Industries MaNGOS software
#
##################################################################################################

# Variables
INSTALL_DIR = '/opt/mangos2_ci_server/'
SYS_USR = 'mangos'
ScriptDev2_lib = 'https://github.com/mangosthree/scripts.git'
host_name = ''
SYS_PASS = ''
SERV_CODE = 'home/' + SYS_USR + '/server/sql/updates/'
_LOC_SQL_UPDATES_ = SERV_CODE + '/server/sql/updates/'
CI_IN_REALM_NAME = ''
wdb = ''
cdb = ''
scd2db = ''
# Menu variables
CI_UPDATE_YN = ''
CI_COMPILE_YN = ''
keep_s_dir = ''
CI_REALM_NAME = ''
ScriptDev2_lib = ''
CI_ACCOUNT_DB = 'localhost'
CI_MANGOS_DB = 'localhost'
CI_MANGOS_DB_PORT = '3306'
CI_REALM_DB_PORT = '3306'
CI_MANGOS_USR = ''
CI_MANGOS_USR_PASS = ''
mysql_root_ci_usr = 'root'
mysql_root_ci_usr_pass = ''
ACC_DATABASE = 'realmd-account'

# Importing all our needed function
from subprocess import call
import subprocess
import shlex
import getpass
import os
import os.path
import urllib2
import time
import glob
import npyscreen

###########################################
#
#  Collective Industries Functions
#
###########################################

# Debug
def debug(var, msg, DEBUG):
    if DEBUG == 1:
        if var == '':
            print msg
        else:
            print var + ' = ' + msg
        raw_input('(Press any key to continue)')

# Sets Realm Name, World DB name, Character DB name, and ScriptDev2 DB name
def setrn():
    global CI_REALM_NAME
    global wdb
    global cdb
    global scd2db
    CI_REALM_NAME = subprocess.check_output(['uname', '-n'])
    wdb = 'mangos-' + CI_REALM_NAME
    cdb = 'characters-' + CI_REALM_NAME
    scd2db = 'scriptdev2-' + CI_REALM_NAME
    debug('wdb', wdb, 1)
    debug('cdb', cdb, 1)
    debug('scd2db', scd2db, 1)

# Handles git commands    
def git_api(command, args):
    subprocess.call(shlex.split('sudo git ' + command + ' ' + args))
            
# CI MANGOS LOGO HERE
# Idea by Levi Modl
# adapted to work with Python by Andrew Malone
def logo():
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

###################################################
##  backport for ubuntu 10                       ##
##  (check_output was introduced in python 2.7)  ##
###################################################
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
    
#######################################################################
##  change directory                                                 ##
##  class provided by                                                ##
##  http://stackoverflow.com/questions/431684/how-do-i-cd-in-python  ##
#######################################################################
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
    
######################################################################
#
# Collective Industries Main Menu
# 
######################################################################
class MangosInstall(npyscreen.NPSApp):
    def main(self):
    
        # Global Variables
        global CI_UPDATE_YN
        global CI_COMPILE_YN
        global keep_s_dir        
        global CI_REALM_NAME
        global ScriptDev2_lib
        global CI_ACCOUNT_DB
        global CI_MANGOS_DB
        global CI_MANGOS_DB_PORT
        global CI_REALM_DB_PORT
        global CI_MANGOS_USR
        global CI_MANGOS_USR_PASS
        global mysql_root_ci_usr
        global mysql_root_ci_usr_pass
        global ACC_DATABASE
        
        mangos = npyscreen.FormMultiPageActionWithMenus(name = 'Collective Industries MaNGOS Insaller') # Creates the form and declarers the type of form
        
        # Realm Name
        CI_IN_REALM_NAME = mangos.add(npyscreen.TitleText, max_height=3, name='Realm Name:', value=CI_REALM_NAME)
        # Installs required programs and also updates any programs that need upgrading
        CI_UPDATE_YN = mangos.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Preform Pre-Install + updates:", 
                values = ["Yes","No"], scroll_exit=True)       
        CI_COMPILE_YN = mangos.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Bypass Compile:", 
                values = ["Yes","No"], scroll_exit=True)
        keep_s_dir = mangos.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Save Source Code:", 
                values = ["Yes","No"], scroll_exit=True)
        #ScriptDev2 Library
        ScriptDev2_lib = mangos.add(npyscreen.TitleSelectOne, max_height=5, value = [1], name='ScriptDev2 Library:',
                values = ["https://github.com/scriptdev2/scriptdev2-cata.git", "https://github.com/mangosthree/scripts.git", "https://github.com/CollectiveIndustries/scripts.git"], scroll_exit=True)                        
        
        # New Page
        NewPage = mangos.add_page()
        """HN = Hostname   DB = Database"""
        # Account Database Hostname
        CI_ACCOUNT_DB = mangos.add(npyscreen.TitleText, name='Account HN', value=CI_ACCOUNT_DB)
        #
        CI_MANGOS_DB = mangos.add(npyscreen.TitleText, name='MaNGOS HN', value=CI_MANGOS_DB)
        CI_MANGOS_DB_PORT = mangos.add(npyscreen.TitleText, name='MaNGOS Port', value=CI_MANGOS_DB_PORT)
        CI_REALM_DB_PORT = mangos.add(npyscreen.TitleText, name='Realm Port', value=CI_REALM_DB_PORT)
        CI_MANGOS_USR = mangos.add(npyscreen.TitleText, name='MySQL UN', value=CI_MANGOS_USR)
        CI_MANGOS_USR_PASS = mangos.add(npyscreen.TitleText, name='UN Pass', value=CI_MANGOS_USR_PASS)      
        mysql_root_ci_usr = mangos.add(npyscreen.TitleText, name='DB Admin UN', value=mysql_root_ci_usr)
        mysql_root_ci_usr_pass = mangos.add(npyscreen.TitleText, name='Admin PW', value=mysql_root_ci_usr_pass)        
        WORLD_DATABASE = mangos.add(npyscreen.TitleText, name='World DB', value=wdb)        
        CHAR_DATABASE = mangos.add(npyscreen.TitleText, name='Char DB', value=cdb)        
        SCRDEV2_DATABASE = mangos.add(npyscreen.TitleText, name='ScriptDev2', value=scd2db)
        ACC_DATABASE = mangos.add(npyscreen.TitleText, name='Account DB', value=ACC_DATABASE)
        mangos.edit()
        
######################################################################
#
# Script Entry Point
#
######################################################################
subprocess.call('clear')
logo()
setrn() # Sets the Realm Name, World Database name, Character Database name, and the Scriptdev2 Database name
print 'Welcome: ' + getpass.getuser()

if getpass.getuser() == 'root':
    print '/!\\ WARNING: Script is being run as root /!\\\n During this script we will change to root as needed so system files do not get messed up during this install procedure'

override = raw_input('Override root security locks-outs? [n] ' )
debug('override', override, 0)
if override == '' or override == 'n':
	print "Root Security Lockout: ENABLED\nthis script will now terminate"
	exit(1) # Exit code 1 (debug info for calling scripts or for user need documentation in readme on exit codes)
 
######################################
##  Calls the Menu and starts it up ##
######################################
debug('', 'Menu starting up', 0)
App = MangosInstall()
App.run()

################################
##  Main Script Installation  ##
################################
debug('CI_UPDATE_YN', str(CI_UPDATE_YN.get_selected_objects()), 0)

if CI_UPDATE_YN.get_selected_objects() == ['Yes']:
    print "We will now begin to process all dependencies required to build the MaNGOS server" 
    print "Running Update as user: " 
    subprocess.call(shlex.split('sudo id -nu')) 
    subprocess.call(shlex.split('sudo apt-get update -q --force-yes'))
    subprocess.call(shlex.split('sudo apt-get dist-upgrade -q --force-yes'))
    subprocess.call(shlex.split('sudo apt-get install -q --force-yes build-essential gcc g++ automake git-core autoconf make patch libmysql++-dev mysql-server libtool libssl-dev grep binutils zlibc libc6 libbz2-dev cmake'))
    # END Preparation
 
if CI_COMPILE_YN.get_selected_objects() == ['No']:
    # TODO: Swap out urls for CI github repo AFTER code clean up and repo creation
    git_api("clone", 'https://github.com/mangosthree/server.git '+SERV_CODE+'/server')
	git_api("clone", 'https://github.com/CollectiveIndustries/Mangos_world_database.git '+SERV_CODE+'/database')
    # Clone ScriptDev2 - execute from within src/bindings directory
    print 'Changing Directory to: ' + SERV_CODE + '/server/src/bindings\nINSTALLING ' + ScriptDev2_lib
    with cd(SERV_CODE + '/server/objdir'):
        git_api('clone', ScriptDev2_lib + ' ./ScriptDev2')
        
    # Tools directory
    git_api('clone', 'https://github.com/mangosthree/tools.git ' + SERV_CODE + '/tools')
    # START compile and begin install
    os.makedirs(os.path.join(SERV_CODE + '/server/', 'objdir'))
    # Change to our compile directory and run the compile
    with cd(SERV_CODE + '/server/objdir'):
        subprocess.call(shlex.split('sudo cmake .. -DCMAKE_INSTALL_PREFIX=' + INSTALL_DIR + ' -DINCLUDE_BINDINGS_DIR=ScriptDev2'))
        subprocess.call(shlex.split('sudo make'))
        subprocess.call(shlex.split('sudo make install'))

#######################
##  Database String  ##
#######################

### TODO: Change all DB strings to DROP IF EXIST then CREATE

# CREATE DATABASE `mangos` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
ADD_MANGOS_MYSQL = ('CREATE DATABASE `' + CHAR_DATABASE + '` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# CREATE DATABASE `characters` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
ADD_MANGOS_MYSQL = ('CREATE DATABASE `' + CHAR_DATABASE + '` DEFAULT CHARACTER utf8 COLLATE utf8_general_ci;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# CREATE DATABASE `realmd` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
ADD_MANGOS_MYSQL = ('CREATE DATABASE `' + ACC_DATABASE + '` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# CREATE DATABASE `scriptdev2` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
ADD_MANGOS_MYSQL = ('CREATE DATABASE `' + SCRDEV2_DATABASE + '` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# CREATE USER 'mangos'@'localhost' IDENTIFIED BY 'mangos';
ADD_MANGOS_MYSQL = ('CREATE USR ' + CI_MANGOS_USR + '@localhost ' + 'IDENTIFIED BY ' + CI_MANGOS_USR_PASS + ';\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `mangos`.* TO 'mangos'@'localhost';
ADD_MANGOS_MYSQL = ('GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `' + WORLD_DATABASE + '`.* TO ' + CI_MANGOS_USR + '@localhost:\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `characters`.* TO 'mangos'@'localhost';
ADD_MANGOS_MYSQL = ('GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `'+CHAR_DATABASE+'`.* TO '+ CI_MANGOS_USR + '@localhost;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `realmd`.* TO 'mangos'@'localhost';
ADD_MANGOS_MYSQL = ('GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `'+ACC_DATABASE+'`.* TO '+ CI_MANGOS_USR + '@localhost;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `realmd`.* TO 'mangos'@'localhost';
ADD_MANGOS_MYSQL = ('GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, LOCK TABLES ON `'+SCRDEV2_DATABASE+'`.* TO '+ CI_MANGOS_USR + '@localhost;\n\n')
mangos_ci_sql_inst.write(ADD_MANGOS_MYSQL)

# Setup realm-list and with iser input
# INSERT INTO `realmlist` VALUES ('MaNGOS', '127.0.0.1', 8085, 0, 2, 0, 0, 0, '');
# TODO: Setup User input Section + loop for manual install of realms to account server
# Finalize the SQL file
mangos_ci_sql_inst.close()
print 'SQL file for MaNGOS DB install has been written to your home directory: [' + "/home/" + SYS_USR + "/mangos-ci-usr.sql" + ']'

# Run the upload
MYSQL_FILE_LOC = '/home/' + SYS_USR + '/mangos.sql'
# TODO: Get MySQL syntax for port number
# Edit -h for configurable host by DB NAME (realmd and mangosd)
# IDEA: Setup host/port for each database (Could be useful in multi server platform) (ENTERPRISE INSTALLER)

# DEPRECIATED os.system('mysql -u ' + mysql_root_ci_usr + ' -p' + mysql_root_ci_usr_pass + ' -h localhost' + ' < ' + MYSQL_FILE_LOC) 
# TODO: Add in -h CONFIG


if keep_s_dir.get_selected_objects()  == ['No']:
    print 'Source code directory will be erased after full install is finished' # Only remove /opt/SOURCE/mangos3_ci_code/*
 