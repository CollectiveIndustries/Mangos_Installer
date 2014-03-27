#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for parsing CI-MANGOS logs and writting them to SQL entrys
#
##################################################################################################

#### USER GLOBALS ####
MYSQL_USR = 'root'
MYSQL_PASS = '1234qwer'
MYSQL_HOST = 'localhost'
MYSQL_DB = 'mangos-dexter'
CI_MANGOS_LOG_LOC = '/opt/mangos3_ci_server/logs'

############################################# DO NOT EDiT BELOW LINE #############################

### IMPORTS ###
from subprocess import call 
import os 
import subprocess 
import shlex 
import getpass 
import time 
import urllib2 
import os.path
import glob

### FUNCTIONS ###

# Collective Industries mysql call
def mysql_call(usr, psw, host, db, sql):
        """Function for Adding sql files to MySQL Host"""
        os.system("mysql -u " + usr + " -p" + psw + " -h " + host + ' ' + db + "  < " + sql )

# mysql_call()

### LOG -> SQL ###
def log2sql(log_file,tmp_sql):
	with open(log_file,'r') as infile:
		with open(tmp_sql,"w") as outfile:
			for i,line in enumerate(infile):
				#split line up and determine where it goes in our log database
				#2014-03-27 13:29:26 SQL ERROR: MySQL server has gone away
				#2014-03-27 13:29:26 SQL: UPDATE realmlist SET realmflags = realmflags | 2 WHERE id = '2'
				sql_list = line.rsplit(":") #chop off the message section and save to a list
				print sql_list #DEBUG string (prints out list)
### LOG FILES ###
#TODO add in a config reader to pull log names from server config
CHAR_LOGS = 'Char.log'
EventAI_LOGS = 'EventAIErrors.log'
SD2_LOGS = 'SD2Errors.log'
WORLD_LOGS = 'World.log'
DB_LOGS = 'DBErrors.log'
GM_LOGS = 'GMs.log'
SERVER_LOGS = 'Server.log'

### globals ###
MYSQL_TABLE_WORLD_LOGS = 'world_logs'

log2sql(CI_MANGOS_LOG_LOC+"/"+DB_LOGS,"/tmp/CI-MANGOS3_DB-logs.sql")#parse the log into the tmp directory