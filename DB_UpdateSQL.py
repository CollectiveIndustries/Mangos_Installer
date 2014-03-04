#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone python code for 
# installing MaNGOS db updates from the SQL/Updates Dir
#
##################################################################################################

# our variables we need later
_LOC_SQL_UPDATES_ = "./server/sql/updates/"
_FILE_TEMP_RAW_ = "./server/sql_updates.tmp"
_FILE_TEMP_SORT_ = "./server/sql_updates_sort.tmp"

# variables starting with _IN_ are user defined 
# other global variables for running the updates are listed at bottom
# _IN_MYSQL_USR_
# _IN_MYSQL_PASS_
# _IN_MYSQL_HOST_
# _IN_MYSQL_DB_MANGOS_
# _IN_MYSQL_DB_CHAR_
# _IN_MYSQL_DB_REALM_
#
# _DB_

# import all of our needed functions
from subprocess import call 
import os 
import subprocess
import sys
import getpass
import time
import glob

# lets clear our screen and give the user some information 
subprocess.call('clear') 
print "Welcome: " + getpass.getuser() 
print "Durring the rest of this script we will install updates to the CI-Mangos server" 


# TODO add port number question for non stadard mysql server setups (also see the os.system(mysql) syntav for port number
_IN_MYSQL_USR_ = raw_input('Database UserName [mangos]: ')
if _IN_MYSQL_USR_ == '':
	_IN_MYSQL_USR_ = 'mangos' #defualt user name
_IN_MYSQL_PASS_ = raw_input('password for '+_IN_MYSQL_USR_+' [mangos]: ')
if _IN_MYSQL_PASS_ == '':
        _IN_MYSQL_PASS_ = 'mangos' #defualt password
_IN_MYSQL_HOST_ = raw_input('Database hostname [localhost]: ')
if _IN_MYSQL_HOST_ == '':
        _IN_MYSQL_HOST_ = 'localhost' #defualt hostname
_IN_MYSQL_DB_MANGOS_ = raw_input('Database MaNGOS [mangos]: ')
if _IN_MYSQL_DB_MANGOS_ == '':
        _IN_MYSQL_DB_MANGOS_ = 'mangos' #defualt name
_IN_MYSQL_DB_CHAR_ = raw_input('Database char [characters]: ')
if _IN_MYSQL_DB_CHAR_ == '':
        _IN_MYSQL_DB_CHAR_ = 'characters' #defualt name
_IN_MYSQL_DB_REALM_ = raw_input('Database realmd [realmd]: ')
if _IN_MYSQL_DB_REALM_ == '':
        _IN_MYSQL_DB_REALM_ = 'realmd' #defualt name
patches = glob.glob(_LOC_SQL_UPDATES_ + '*.sql')
patches = sorted(patches)

print "Starting Patching Process"
_DB_ = ''

for x in patches: #set up a loop to run through the current working directory
  print "Patching File: " + x #tell user what file is being added to the Database
  db = x.split("_")[2].replace('.sql', '')#this is for the Mangos FileName structure we have to sort them and find the database names
  if db == 'characters':
  	_DB_  = _IN_MYSQL_DB_CHAR_
  if db == 'realmd':
        _DB_ = _IN_MYSQL_DB_REALM_
  if db == 'mangos':
        _DB_ = _IN_MYSQL_DB_MANGOS_  #block was for determining the database from the file name and the users input
  os.system("mysql -u " +_IN_MYSQL_USR_ + " -p" + _IN_MYSQL_PASS_ + " -h " + _IN_MYSQL_HOST_ + " -v " + _DB_ + " < " + x) 
#this is the MySQL work horse this is the one line that makes everything work
