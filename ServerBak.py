#!/usr/bin/env python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone 
# python code for pulling a Mangos backup and saving the backup in either a local directory
# or a remote server (easy way to clone MaNGOS World server configurations)
#
##################################################################################################

import os
import zipfile
import subprocess 
import shlex 

#GLOBAL VARIABLES
SSH_REMOTE = ""
SSH_PORT = ""


def main(): #main function all commands will be called from here
    DIR_IN = raw_input ("Please enter the dir you wish to ZIP: ")
    ZIP_PATH = raw_input("Name full path of ZIP File: ")		
    zipper(DIR_IN, ZIP_PATH)
    REMOTE_USER = raw_input("Remote User: ")
    #scp local_file user@remote_host:remote_file
    remote_file_name = ZIP_PATH.split('/')
    #call SCP and dump zip file in Remote Dir
    subprocess.call(shlex.split('scp -P '+SSH_PORT+' '+ZIP_PATH+' '+REMOTE_USER+'@'+SSH_REMOTE+':'+remote_file_name[-1]))

def zipper(dir, zip_file):
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in os.walk(dir):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
            print f
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

def mysql_bak(usr_name, usr_pass, db_name)
	subprocess.call(shlex.split("mysqldump --user="+usr_name+" --password"+usr_pass+" "+db_name))
	
if __name__ == '__main__':
    main()

