
## GLOBAL switch ##
_DEBUG_ = False

## debug output ##
def debug(string,value):
        if _DEBUG_ is True:
                print "%s DEBUG: %s %s" % (TimeStamp(), string, value)
