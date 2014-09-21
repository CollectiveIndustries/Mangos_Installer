from collections import defaultdict

## Global Settings ##
INSTALL_DIR = '/opt/ci_mangos3/'
SYS_USR = 'mangos'
SERV_HOME = '/home/' + SYS_USR
CODE_BASE = SERV_HOME + '/SOURCE'

			## /!\ WARNING: ADVANCED SETTINGS /!\ ##


## incorectly setting ANY of the following settings will render the installer useless ##
## please be carefull when adjusting these settings ##
## This means you Marvy Snuffleson of Kansass City, MO!!!!!
## not exactly sure who that is O_e
INSTALLER_LST = [       ## option_name                  ## VALUES [MSG, (0 = input, 1 = info), OPTION_VALUE, PRIORITY] 
			("REALM_NAME",			"Realm Name? "),
			("REALM_NAME",			0),
			("REALM_NAME",			""),
			("REALM_NAME",			100),
			
		        ("REALM_DB_HOST",		"Host name for account DB? "),
			("REALM_DB_HOST",		0),
			("REALM_DB_HOST",		"localhost"),
			("REALM_DB_HOST",		198),
			
			("ACCOUNT_DB_PORT",		"Port number for account DB? "),
			("ACCOUNT_DB_PORT",		0),
			("ACCOUNT_DB_PORT",		"3306"),
			("ACCOUNT_DB_PORT",		199),
			
            		("M_DB_HOST",			"Host name for WORLD DB? "),
			("M_DB_HOST",			0),
			("M_DB_HOST",			"localhost"),
			("M_DB_HOST",			196),
			
            		("M_DB_PORT",			"Port number for WORLD DB?"),
			("M_DB_PORT",			0),
			("M_DB_PORT",			"3306"),
			("M_DB_PORT",			197),
			
            		("WORLD_DB",			"New World Database: "),
			("WORLD_DB",			0),
			("WORLD_DB",			"world"),
			("WORLD_DB",			210),
			
			("CHAR_DB",			"New Chaharacters Database: "),
			("CHAR_DB",			0),
			("CHAR_DB",			"characters"),
			("CHAR_DB",			211),
			
            		("SCRIPTS_DB",			"New ScriptDev2 Database: "),
			("SCRIPTS_DB",			0),
			("SCRIPTS_DB",			"scriptdev2"),
			("SCRIPTS_DB",			212),
			
            		("ACCOUNT_DB",			"New Account Database: "),
			("ACCOUNT_DB",			0),
			("ACCOUNT_DB",			"realmd-accounts"),
			("ACCOUNT_DB",			213),
			
            		("SRV_VER",			"MaNGOS version (1 vanilla - 5 MoP) "),
			("SRV_VER",			0),
			("SRV_VER",			"4"),
			("SRV_VER",			501),
			
            		("REALM_ID",			"RealmID Number "),
			("REALM_ID",			0),
			("REALM_ID",			"1"), # default realm 1
			("REALM_ID",			500),
			
            		("INSTALL_DIR",			"Instalation Destination: "),
			("INSTALL_DIR",			0),
			("INSTALL_DIR",			INSTALL_DIR),
			("INSTALL_DIR",			400),
			
			("MANGOS_SYS_GROUP",		"New System Group for MaNGOS"),
			("MANGOS_SYS_GROUP",		0),
			("MANGOS_SYS_GROUP",		"mangosd"),
			("MANGOS_SYS_GROUP",		100),
			
			("REALMD_SYS_GROUP",		"New System Group for RealmD"),
			("REALMD_SYS_GROUP",		0),
			("REALMD_SYS_GROUP",		"realmd"),
			("REALMD_SYS_GROUP",		101),
			
            		## DATABASE USERS AND PASSWORDS ##
            		("MYSQL_MANGOS_ADMIN_USR",	"MySQL ADMIN user for the MANGOSD host: "),
			("MYSQL_MANGOS_ADMIN_USR",	0),
			("MYSQL_MANGOS_ADMIN_USR",	"root"),## MANGOS and REALMD may be seprate hosts
			("MYSQL_MANGOS_ADMIN_USR",	200),
			
            		("MYSQL_MANGOS_ADMIN_PASS",	"MySQL ADMIN password for the MAGOSD host: "),
			("MYSQL_MANGOS_ADMIN_PASS",	0),
			("MYSQL_MANGOS_ADMIN_PASS",	""),
			("MYSQL_MANGOS_ADMIN_PASS",	201),
			
            		("MYSQL_REALMD_ADMIN_USR",	"MySQL ADMIN user for the REALMD host: "),
			("MYSQL_REALMD_ADMIN_USR",	0),
			("MYSQL_REALMD_ADMIN_USR",	"root"),
			("MYSQL_REALMD_ADMIN_USR",	202),
			
            		("MYSQL_REALMD_ADMIN_PASS",	"MySQL ADMIN password for the REALMD host: "),
			("MYSQL_REALMD_ADMIN_PASS",	0),
			("MYSQL_REALMD_ADMIN_PASS",	""),
			("MYSQL_REALMD_ADMIN_PASS",	203),
			
            		("MYSQL_MANGOS_USR",		"New MaNGOS user (system and databases): "),
			("MYSQL_MANGOS_USR",		0),
			("MYSQL_MANGOS_USR",		SYS_USR),## MANGOS Database and server may be on a seprate host
			("MYSQL_MANGOS_USR",		204),
			
            		("MYSQL_REALMD_USR",		"New REALMD user (System and DataBases): "),
			("MYSQL_REALMD_USR",		0),
			("MYSQL_REALMD_USR",		SYS_USR),## REALMD Database and server may be on diffrent host
			("MYSQL_REALMD_USR",		206),
			
            		("MYSQL_MANGOS_PASS",		"New MaNGOS password (DataBase only): "),
			("MYSQL_MANGOS_PASS",		0),
			("MYSQL_MANGOS_PASS",		""),#THE NEXT 2 VALUES will be PASSED to the MYSQL-PY connector to
			("MYSQL_MANGOS_PASS",		205),
			
            		("MYSQL_REALMD_PASS",		"New REALMD password (DataBase only): "),
			("MYSQL_REALMD_PASS",		0),
			("MYSQL_REALMD_PASS",		""),#this has to be passed to the configuration scripts
			("MYSQL_REALMD_PASS",		207),
			
            		## GIT CODE LOCATIONS ##
            		("GIT_REPO_CI_SERVER",		"LOCAL github repository:[Server] "),
			("GIT_REPO_CI_SERVER",		1),
			("GIT_REPO_CI_SERVER",		CODE_BASE+"/server"),
			("GIT_REPO_CI_SERVER",		900),
			
            		("GIT_REPO_CI_DBS",		"LOCAL github repository:[DataBase] "),
			("GIT_REPO_CI_DBS",		1),
			("GIT_REPO_CI_DBS",		CODE_BASE+"/database"),
			("GIT_REPO_CI_DBS",		900),
			
            		("GIT_REPO_CI_SD2",		"LOCAL github repository:[ScriptDev Library] "),
			("GIT_REPO_CI_SD2",		1),
			("GIT_REPO_CI_SD2",		CODE_BASE+"/server/src/bindings/ScriptDev2"), ## SCRIPT DEV LI$
			("GIT_REPO_CI_SD2",		900),
			
            		("GIT_REPO_CI_TOOLS",		"LOCAL github repository:[Extra Tools] "),
			("GIT_REPO_CI_TOOLS",		1),
			("GIT_REPO_CI_TOOLS",		CODE_BASE+"/tools"),
			("GIT_REPO_CI_TOOLS",		900),
			
            		("GIT_REPO_CI_WEB",		"LOCAL github repository:[Web Site] "),
			("GIT_REPO_CI_WEB",		1),
			("GIT_REPO_CI_WEB",		CODE_BASE+"/web"),
			("GIT_REPO_CI_WEB",		900),
			
            		## FILE STRUCTURE ##

            		("MANGOS_LOGS_DIR",		"Logs Directory (relitive to INSTALL_DIR) "),
			("MANGOS_LOGS_DIR",		0),
			("MANGOS_LOGS_DIR",		"logs"),# Path is relitave to the INSTALL_DIR
			("MANGOS_LOGS_DIR",		900),
			
            		("MANGOS_DATA_DIR",		"Data Directory (relitive to INSTALL_DIR) "),
			("MANGOS_DATA_DIR",		0),
			("MANGOS_DATA_DIR",		"data"), # Path is relitave to the INSTALL_DIR
            		("MANGOS_DATA_DIR",		900),
			]
## build the dictionary for the installer >..< why we have to do it this way is beyond me ##

def BuildSettings( lst_input ):
	list_to_dictionary = defaultdict(list)
	for k, v in lst_input:
        	list_to_dictionary[k].append(v)
	return list_to_dictionary #return the entire thing back to the main process

## setts a new value to the Settings List ##
def set_option(k,v,defualt,struct):
	"""sets a new value (v) for KEY (k) passed to the function if value (v) is empty use defualt"""
	for key in struct.keys():
        	if key == k:
                	if v == '': ## taking into account the items above the value we want is going to be [2] in our Dictionary of Lists
                                struct[key][2] = defualt
                        else:
                                struct[key][2] = v
	return struct ## return the newly written values ##
