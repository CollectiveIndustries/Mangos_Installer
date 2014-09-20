#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2014 Collective Industries 
# 
# AUTHOR: Andrew Malone 
#  
# TITLE: Environment
#
# PURPOSE: environmetn related code for MaNGOS Installer
#
#
##################################################################################################

## Install Libraries ##
import debug as bugs

## OS Imports ##
import getpass

## Function Definitions ##

def TimeStamp():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

def HostName():
	hostname = subprocess.check_output(["uname", "-n"])
	if hostname[-1] == '\n':
		bugs.debug("HostName() []:",hostname[:-1])
		hostname = hostname[:-1]
	return hostname #return only the host name no New line
	
## CONSOLE SIZE ##
def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])
	
## Grab currant System User ##
def UserName():
	return getpass.getuser()

## Clean a full directory path ##
def clean_dir(path):
	for file in os.listdir(path):
		file_path = os.path.join(path, file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)# Clean out files
				cur_pos(1,26,TimeStamp()+" Unlinking: "+file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)# delete folders recursively
				cur_pos(1,26,TimeStamp()+" Removing Directory Tree: "+file_path)
		except Exception, e:
			print e
