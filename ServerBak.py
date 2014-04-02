#!/usr/bin/env python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for pulling a Mangos backup and saving the backup in either a local directory
# or a remote server (easy way to clone MaNGOS World server configurations)
#
##################################################################################################

## MYSQL SERVER SETTINGS ##
#dumps all databases#
MYSQL_BACK_USR = "BACKUP"
MYSQL_BACK_PASS = "mapujaVezitiGI54Huwu8oQIVEsIxA"

## DIRECTORY LIST TO BACK UP ##
LOCAL_DIR_LIST = ["/opt/mangos3_ci_server/logs",
		  "/var/www",
		  "/home/im-support",
		  "/home/icinga",
#		  "/var/log",
		  "/var/teamspeak3-server_linux-x86"];

## DESTINATION FOR BACK-UP ZIP ##
BACKUP_DEST = "/var/www"

## DAEMON MODE ##
#
# this will give you two running modes:
# 1) local only
# 2) remote (MUST HAVE KEY PAIR FOR BACKUP USER FOR AUTOMATION MAKE SURE YOU HAVE ONE BEFORE SETTING THIS SECTION UP)
# if daemon mode is enabled and no key pair has been set up the script will ask the user for a password 
# if you want a fully autmoted back up with remote support you need to first generate an ssh key for the user/host
# by default this script is configured to run in daemon mode localy after setting all of your back up option above
# you can add this script to the crontab to run it automaticly
MODE = "local" #will disable SCP file copy set to "remote" for scp copy
REMOTE_KEY_INSTALLED = "false" #if daemon is enabled and mode is remote and this is false errors will happen 
DAEMON_ENABLED = "true" #set this to true to run script with a cron job

## REMOTE SETTINGS ##
SCP_HOST = ""
SCP_PORT = "22"
SCP_USER = "" #if blank sets current user as default


################################ DO NOT EDIT BELOW THIS LINE ################################################################

import os
import zipfile
import subprocess
import shlex
import datetime # needed for time stamp on SQL + ZIP dump
import getpass

def debug(string,value):
	print "%s DEBUG: %s %s" % (TimeStamp(), string, value)
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

def DirName(path):
	result = path.replace('/','-') #return the last part of the directory name
	debug("DirName() Result:",result)
	return result[:-1]

def TimeStamp():
	result = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
	return result

def HostName():
	hostname = subprocess.check_output(["uname", "-n"])
	if hostname[-1] == '\n':
		hostname = hostname[:-1]
	return hostname #return only the host name no New line

def UserName():
	result = getpass.getuser()
	return result

def zipper(dir, zip_file):#show me that array
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in os.walk(dir):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
            print TimeStamp()+" "+f #print out file name in sub directory with the time stamp for logging
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

def mysql_bak(usr_name, usr_pass,sql_dump_loc):
	dump_name = sql_dump_loc+"/"+usr_name+"_ALL_DATABASES_"+HostName()+"_"+TimeStamp()+".sql"
	print "%s Dumping all databases to --> %s" % (TimeStamp(),dump_name)
	subprocess.call(shlex.split("mysqldump --all-databases --user="+usr_name+" --password="+usr_pass+" --result-file="+dump_name))
	print "%s [DUMPED]" % (TimeStamp())

def PackList(full_dump_name):#dump our package list to get backed up
	debug("PackageList","DUMPED")
	#checkoutput()
	install_list = subprocess.check_output(["dpkg","--get-selections"])#grab out put of the command and lets get a list ready
	with open(full_dump_name,"w") as outfile:
		outfile.write(install_List)
#	subprocess.call(shlex.split("dpkg --get-selections > /tmp/INSTALL_LIST"+TimeStamp()+"_"+HostName()+".lst"))

#BACKUP_FILE,SCP_USER,SCP_PORT,SCP_HOST
def scp(filename,scp_user,scp_port,scp_host)
	#give scp variables and start file transfer
	scp_path = filename.split("\\")
	scp_filename = scp_path[-1]
	subprocess.call(shlex.split("scp -P "+scp_port+" -Cv "+filename+" "+scp_user+"@"+scp_host+":~\\"+scp_filename))

def scp_getinfo():
	host = raw_input("Remote Hostname: ")
	port = raw_input("Remote Host PORT: [22] ")
	user = raw_input("Remote Host USER: ["+UserName()+"] ")
	#scp_pass = raw_input("Remote Password: ") #will be automaticly asked when SCP is called
	#set defaults if no option was chosen
	if port == "":
		port = "22"
	if user == "":
		user = UserName()
	return [user,port,host]
def main(): #main function all commands will be called from here
	subprocess.call(shlex.split('sudo rm -Rf /tmp/*'))#do a full temp wipe before we dump our backups
	print "Backup started: "+TimeStamp()
	PackList(BACKUP_DEST+"/"+TimeStamp()+"_"+HostName()+"INSTALL_LIST.lst")
	zip_name = BACKUP_DEST+"/"+TimeStamp()+"_"+HostName()+"_"+UserName()+".zip"
	mysql_bak(MYSQL_BACK_USR,MYSQL_BACK_PASS,"/tmp") #dump our SQL database to local directory and get it ready to  include in our zipper
	print "%s [DUMPING] %s" % (TimeStamp(),LOCAL_DIR_LIST)
	for name in LOCAL_DIR_LIST:
		sub_zips = "/tmp/"+DirName(name)+"_"+TimeStamp()+"_"+HostName()+"_"+UserName()+".zip"
		print TimeStamp()+" [ZIPPING] "+name #give user a time stamp for each zip file
		zipper(name, sub_zips)
		print TimeStamp()+" [ZIP-DONE] "+name
	BACKUP_FILE = BACKUP_DEST+"/FULL_SERVER_"+HostName()+"_"+TimeStamp()+"_"+UserName()+".zip" 
	zipper("/tmp",BACKUP_FILE)
	print "Backup Ended: "+TimeStamp()
	print "Wipping /tmp: "+TimeStamp()
	subprocess.call(shlex.split('sudo rm -Rf /tmp/*'))#do a full temp wipe
	print "your backup is located: "+BACKUP_FILE
	if MODE == "remote" and DAEMON_ENABLED == "false": #manualy ran
		SCP_OPT = raw_input("Would you like to push data to remote SSH Server? [y] ")
		if SCP_OPT == "":
			info_lst_scp = scp_getinfo()
			SCP_HOST = info_lst_scp[2]
			SCP_PORT = info_lst_scp[1]
			SCP_USER = info_lst_scp[0]
			scp(BACKUP_FILE,SCP_USER,SCP_PORT,SCP_HOST)#full file and path to backup
		elif SCP_OPT == "y":
			info_lst_scp = scp_getinfo()
			SCP_HOST = info_lst_scp[2]
			SCP_PORT = info_lst_scp[1]
			SCP_USER = info_lst_scp[0]
			scp(BACKUP_FILE,SCP_USER,SCP_PORT,SCP_HOST)#full file and path to backup
	elif MODE == "remote" and DAEMON_ENABLED == "true":
		#is an SSH_KEY been installed? (user confimed at top of settings)
		if SCP_USER == "":
			SCP_USER = UserName()
			
		if REMOTE_KEY_INSTALLED == "true":
			scp(BACKUP_FILE,SCP_USER,SCP_PORT,SCP_HOST)
		else
			print "MODE is remote but REMOTE_KEY_INSTALLED is false make sure you have a key setup and the propper user and password is set at the top of this script"
			sys.exit("Bad Global Config Option: [TERMINATING]")
	elif
		print "Remote DISABLED"
	print "Backup complete at: %s" % (TimeStamp())
	
if __name__ == '__main__':
    main()

