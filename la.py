'''A better version of the builtin "dir", place in your .pythonrc.py'''

# >>> from user import la
# >>> import wx
# >>> la(wx, "open")
# ART_FILE_OPEN
# ART_FOLDER_OPEN
# EVT_MENU_OPEN
# ID_OPEN
# OPEN
# Process_Open
# wxEVT_MENU_OPEN
# >>> 

def la(obj, key=None, ignore_case=1):
    '''List all attributes of object'''
    import re
    if key:
        if ignore_case:
            flags = re.I
        else:
            flags = 0
        func = re.compile(key, flags).search

    else:
        func = None
    print "\n".join(filter(func, dir(obj)))
