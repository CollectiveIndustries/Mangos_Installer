#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2014 Collective Industries 
# 
# AUTHOR: Andrew Malone 
#  
# TITLE: gui
#
# PURPOSE: all gui related code for the MaNGOS Installer
#
#
##################################################################################################

## MANGOS Installer libraries ##
from mlib import colors ## COLOR definitions ##
import environment as env
import settings
import debug as bugs

## standard OS Libraries ##
import os

## reset cursor postion in terminal ##
def cur_pos(x_pos,y_pos,MSG,color):
	"""Function to set cursor position"""
	if not bugs._DEBUG_:
		print "\033[%s;%sH\x1b[%sm %s \x1b[0m" % (y_pos,x_pos,color,MSG) #set cursor to X,Y pos and print MSG
	else:
		print "%s" % (MSG)

# CI MANGOS LOGO HERE
# Idea by Levi Modl
# adapted to work with Python by Andrew Malone
# color implimented 9-15-2014 sugested by William Baggett 
def logo():                                                                              ## PRINTS OUT WHITE BOARDER ##
	print "\x1b[0;92;40m                                                              \x1b[0;32;47m  \x1b[0m" #bright green on black no formatting
	print "\x1b[0;92;40m CCCCC       IIIIIIIII                                        \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC             III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC     ====    III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC     ====    III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC             III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40mCCC CCC         III                                           \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;92;40m CCCCC       IIIIIIIII     \x1b[0mhttp://ci-main.no-ip.org/          \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m                                                              \x1b[0;32;47m  \x1b[0m" ## MANGOS LOGO COLORING ##
	print "\x1b[0;91;44mMM   MM         NN   NN  GGGGG   OOOO   SSSSS                 \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM         NN   NN GGG GGG OO  OO SSS SSS                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMMM MMM         NNN  NN GGG GGG OO  OO SSS                    \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM M MM         NNNN NN GGG     OO  OO  SSS                   \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM M MM  AAAAA  NN NNNN GGG     OO  OO   SSS                  \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM M MM A   AAA NN  NNN GGGGGGG OO  OO    SSS                 \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM     AAA NN   NN GG  GGG OO  OO     SSS                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM AAAAAAA NN   NN GGG GGG OO  OO SSS SSS                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44mMM   MM AA  AAA NN   NN  GGGGGG  OOOO   SSSSS                 \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m        AA  AAA                                               \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m        AAAAAA                                                \x1b[0;32;47m  \x1b[0m"
	print "\x1b[0;91;44m                           http://www.getmangos.co.uk/        \x1b[0;32;47m  \x1b[0m"
	print ""
	(width, height) = env.getTerminalSize()
	print "\x1b[0;32;47m" # White block border #
	for x in range(0,65):
		print "\033[%s;%sH " % (25,x)
	print "\x1b[0m"
# END LOGO

## Builds the Text based GUI ##
def reset_scrn(options):
	os.system('cls' if os.name == 'nt' else 'clear')
        logo()
	prt_dict(options,5)

## print out the Settings List ##
def prt_dict(stuff,start):
	"""prints out key value pairs on seprate lines"""
	(width, height) = env.getTerminalSize()
	x_pos = width - 80
	y_pos = start
	print "\x1b[4;32;40m"
	print "\033[%s;%sH%s" % (start,x_pos,"-=/\=-          MaNGOS Install Options          -=/\=-")
	print "\x1b[0m"
	for key,value in sorted(stuff.items(), key=lambda e: e[1][3]): ## Sort the list for the display ##	
		y_pos += 1
		print "\033[%s;%sH     %s" % (y_pos,x_pos,key)
		print "\033[%s;%sH%s" % (y_pos,x_pos+30,value[2])

