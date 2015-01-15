[![Build Status](https://travis-ci.org/CollectiveIndustries/Mangos_Installer.svg?branch=master)](https://travis-ci.org/CollectiveIndustries/Mangos_Installer)
Mangos Installer 
================

Collective Industries is proud to present the new Unified MaNGOS Installer.
installing mangos has never been this easy before.

##INSTALL
In a bash shell you can run the mangos python installer to set up the mangos software 
simply call the installer after checking permissions on the file
on a shell line you can use these commands to to run your setup
chmod a+x ./*.py
this will make all of the python scripts executable for all users
./mangos-ci_install.py
this will run the installer which will walk you through the compile and then down load map data for you
it will also set up databases and create a user for you

##MANUAL INSTALLATIONS
If you prefer to do this by hand or for some reason the install script does not work for your platform a detailed installation can be found in PDF under the docs directory
as of right now the installation instructions are Ubuntu based.
..* most of the installation steps are completely different and have changed to the point of needing a new Guide 
..* RPM based Distro (ClearOS) will be used for this guide 
..* also plans for a ClearOS Module and LDAP account integration are on the white board so adding a realm would be as simple as logging into the ClearOS back end and setting up the settings for the realm
..* all account based information (names + passwords + email + UUID) should be kept in LDAP while all other details be kept in MySQL 
##NOTES
some things have changed in the newer version of MaNGOS.
..* during compile you no longer to need to APPLY Patches for the SD2 Library. this means you longer need to use the (git am src/bindings/ScriptDev2/pathces/MaNGOS-*) commands
..* CMAKE includes have changed a little bit from the first set of documentation ([root@demo _build]# cmake -DCMAKE_BUILD_TYPE=release -DACE_USE_EXTERNAL=0 -DCMAKE_INSTALL_PREFIX=/opt/mangos -DINCLUDE_BINDINGS_DIR=ScriptDev2 ..)
..* PCH  option --> Pre Compiled Headers are faster to process for the compiler this can be specified using -DPCH=1 for TRUE or -DPCH=0 for FALSE
..* TBB Intel® Threading Building Blocks (Intel® TBB) lets you easily write parallel C++ programs that take full advantage of multicore performance found [here](https://www.threadingbuildingblocks.org/ "TBB Home Page")

##TODO
set up a remote MySQL database installer that will connect your mangos realm (world server) to your realmd (account) server
set up config file editor to make configuring mangos easier
also set up a daemon installer to have mangos run in a screen on start up or have the screen be dumped to NULL as there is log files in the logs directory

add an installer for the icinga tool package for server monitoring (python)

##CREDITS
see the CONTRIBUTORS.rst
