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

# import all of our needed libraries
import os 
import sys
import glob
## need to write a I/O plugin for displaying feed back ##
# import 

def patch_db(_LOC_SQL_UPDATES_,_DB_LST_,_DB_CREDS_)
	""" This function takes 2 lists as its input and a file path
	the file path is for the SQL updates for the mangos updates
	the first list is for the databases (this should be built and
	set from the main program) the second list is the server
	connection string the primary goal of this function is to 
	apply SLQ updates for the Database in a set order """

	patches = glob.glob(_LOC_SQL_UPDATES_ + '*.sql')
	patches = sorted(patches) ## this step is important the order of the patches matter on the server
	 "Starting Patching Process"
	_DB_ = ''
	
	for x in patches: #set up a loop to run through the current working directory
		print "Patching File: " + x #tell user what file is being added to the Database
		db = x.split("_")[2].replace('.sql', '')#this is for the Mangos FileName structure we have to sort them and find the database names
		if db == 'characters':
			DB_  = _DB_LST_[0] ## grab first entry on the List for the Char DB
		if db == 'realmd':
			_DB_ = _DB_LST_[1] ## grab the second list entry for the realmd db
		if db == 'mangos':
			_DB_ = _DB_LST_[2] ## grab the 3rd list entry for the mangos db
		os.system("mysql -u " +_DB_CREDS_[0] + " -p" + _DB_CREDS_[1] + " -h " + _DB_CREDS_[2] + " -v " + _DB_ + " < " + x) 
		#this is the MySQL work horse this is the one line that makes everything work
