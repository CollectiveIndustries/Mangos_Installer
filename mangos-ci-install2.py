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
# Menu variables
CI_UPDATE_YN = 1
CI_COMPILE_YN = 1
keep_s_dir = 1

# Importing all our needed function
from subprocess import call
import subprocess
import shlex
import getpass
import os
import urllib2
import npyscreen

###########################################
#
#  Collective Industries Functions
#
###########################################

# Debug
def debug(var, msg, DEBUG):
    if DEBUG == '1':
        if var == '':
            print msg
        else:
            print var + ' = ' + msg
        raw_input('(Press any key to continue)')
        
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

###############################################
# backport for ubuntu 10
# (check_output was introduced in python 2.7)
###############################################
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
    
###################################################################
# change directory
# class provided by
# http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
###################################################################
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
    def MainMenu(self):
    
        # Global Variables
        global CI_UPDATE_YN
        global CI_COMPILE_YN
        global keep_s_dir        
        
        mangos = npyscreen.Form(name = 'Collective Industries MaNGOS Insaller') # Creates the form and declarers the type of form
        
        CI_UPDATE_YN = mangos.add(npyscreen.TitleSelectOne, max_height=-2, value=[1], name='Preform Pre-Install + updates',
            values=['Yes', 'No'], scroll_exit=True)
        CI_COMPILE_YN = mangos.add(npyscreen.TitleSelectOne, max_height=-2, value=[1], name='Bypass compile',
            values=['Yes', 'No'], scroll_exit=True)
        keep_s_dir = mangos.add(npyscreen.TitleSelectOne, max_height=-2, value=[1], name='Would you like to save source code',
            values=['Yes', 'No'], scroll_exit=True)
         
        entry()
######################################################################
#
# Script Entry Point
#
######################################################################
def entry():
    debug('CI_UPDATE_YN', CI_UPDATE_YN, 1)

    if CI_UPDATE_YN == 0:
        print "We will now begin to process all dependencies required to build the MaNGOS server" 
        print "Running Update as user: " 
        subprocess.call(shlex.split('sudo id -nu')) 
        subprocess.call(shlex.split('sudo apt-get update -q --force-yes'))
        subprocess.call(shlex.split('sudo apt-get dist-upgrade -q --force-yes'))
        subprocess.call(shlex.split('sudo apt-get install -q --force-yes build-essential gcc g++ automake git-core autoconf make patch libmysql++-dev mysql-server libtool libssl-dev grep binutils zlibc libc6 libbz2-dev cmake'))
        # END Preparation
    
    if CI_COMPILE_YN == 1:
        #os.makedirs(os.path.join(SERV_CODE)) #main code directory
        print "Directory paths created for install and compile"
    
    if keep_s_dir == 1:
        print 'Source code directory will be erased after full install is finished' # Only remove /opt/SOURCE/mangos3_ci_code/*


print 'Welcome: ' + getpass.getuser()

if getpass.getuser() == 'root':
    print '/!\\ WARNING: Script is being run as root /!\\\n During this script we will change to root as needed so system files do not get messed up during this install procedure'

override = raw_input('Override root security locks-outs? [n] ')

debug('override', override, 1)
if override == ' ' or override == 'n':
    print 'Root Security Lockout: ENABLED\nthis script will now terminate'
    exit(1)

debug('', 'Menu starting up', 1)
App = MangosInstall()
App.run() 