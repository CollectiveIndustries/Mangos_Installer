#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone
# python functions standard to CI-MaNGOS update,install, backups
#
#################################################################################################



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
def git_api(command, args):
	"""Function for handling git commands"""
	subprocess.call(shlex.split('sudo git '+command+' '+args))

# git_api()

#mysql_update()
def mysql_update(update_path, usr_name, usr_pwd, db_list):
	"""mysql update api for MaNGOS database"""
	with cd(update_path):
		patches = glob.glob('*.sql')
	patches = sorted(patches)#sort the patches to upload in correct order
	print "Starting Patching Process"
	_DB_ = ''
	# PatchFile Formatting 12752_01_mangos_reputation_spillover_template.sql
	for x in patches: #set up a loop to run through the current working directory
		print "Patching File: " + x #tell user what file is being added to the Database
		db = x.split("_")[2].replace('.sql', '')#this is for the Mangos FileName structure we have to sort them and find the database names
		print "Selecting Database: " + db
		if db == 'characters':
			_DB_  = db_list[0]
		if db == 'realmd':
			_DB_ = db_list[1]
		if db == 'mangos':
			_DB_ = db_list[2]  #block was for determining the database from the file name and the users input
	mysql_call(usr_name, usr_pwd, 'localhost', _DB_, update_path + x)#no host config set up yet
