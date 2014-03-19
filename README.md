Mangos Installer
================

Collective Industries is proud to present the new Unified MaNGOS Installer.
installing mangos has never been this easy before.

INSTALL
=======
In a bash shell you can run the mangos pythin installer to set up the mangos software 
simply call the installer after checking permissions on the file
on a shell line you can use these commands to to run your setup
chmod a+x ./*.py
this will make all of the pythin scripts exxacutable for all users
./mangos-ci_install.py
this will run the installer which will walk you through the compile and then down load map data for you
it will also set up databases and create a user for you

TODO
====
set up a remote MySQL database installer that will connect your mangos realm (world server) to your realmd (account) server
set up config file editor to make configuring mangos easier
also set up a daemon installer to have mangos run in a screen on start up or have the screen be dumped to NULL as there is log files in the logs directory
