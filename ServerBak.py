#!/usr/bin/env python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for pulling a Mangos backup and saving the backup in either a local directory
# or a remote server (easy way to clone MaNGOS World server configurations)
#
##################################################################################################

## SSH SETTINGS ##
#SSH_REMOTE = ""
#SSH_PORT = ""

## MYSQL SERVER SETTINGS ##
#dumps all databases#
MYSQL_BACK_USR = "admiral"
MYSQL_BACK_PASS = "stu475r4.0.0.5"

## DIRECTORY LIST TO BACK UP ##
LOCAL_DIR_LIST = ["/opt/mangos3_ci_server/logs",
		  "/var/www",
		  "/home/im-support",
		  "/home/icinga",
		  "/var/log",
		  "/var/teamspeak3-server_linux-x86"];

## DESTINATION FOR BACK-UP ZIP ##
BACKUP_DEST = "/var/www"

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
            print f #print out file name in sub directory
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

def mysql_bak(usr_name, usr_pass,sql_dump_loc):
	dump_name = sql_dump_loc+"/"+usr_name+"_ALL_DATABASES_"+HostName()+"_"+TimeStamp()+".sql"
	print "%s Dumping all databases to --> %s" % (TimeStamp(),dump_name)
	subprocess.call(shlex.split("mysqldump --user="+usr_name+" --password="+usr_pass+" --all-databases > "+dump_name))
	print "%s [DUMPED]" % (TimeStamp())

def PackList():#dump our package list to get backed up
	debug("PackageList","DUMPED")
	subprocess.call(shlex.split("dpkg --get-selections > /tmp/INSTALL_LIST"+TimeStamp()+"_"+HostName()+".lst"))

def main(): #main function all commands will be called from here
	subprocess.call(shlex.split('sudo rm -Rf /tmp/*'))#do a full temp wipe before we dump our backups
	print "Backup started: "+TimeStamp()
	PackList()
	zip_name = BACKUP_DEST+"/"+TimeStamp()+"_"+HostName()+"_"+UserName()+".zip"
	mysql_bak(MYSQL_BACK_USR,MYSQL_BACK_PASS,"/tmp") #dump our SQL database to local directory and get it ready to  include in our zipper
	print "%s [DUMPING] %s" % (TimeStamp(),LOCAL_DIR_LIST)
	for name in LOCAL_DIR_LIST:
		sub_zips = "/tmp/"+DirName(name)+"_"+TimeStamp()+"_"+HostName()+"_"+UserName()+".zip"
		print "%s ZIPPING: $s" % (TimeStamp(), name) #give user a time stamp for each zip file
		zipper(name, sub_zips)
		print "%s ZIP-DONE: %s" (TimeStamp(), name)
	zipper("/tmp",BACKUP_DEST+"/FULL_SERVER_"+HostName()+"_"+TimeStamp()+"_"+UserName()+".zip")
	print "Backup Ended: "+TimeStamp()
	print "Wipping /tmp: $s" % (TimeStamp())
	subprocess.call(shlex.split('sudo rm -Rf /tmp/*'))#do a full temp wipe
	print "your backup is located: "+BACKUP_DEST+"/FULL_SERVER_"+HostName()+"_"+TimeStamp()+"_"+UserName()+".zip"

	
if __name__ == '__main__':
    main()

