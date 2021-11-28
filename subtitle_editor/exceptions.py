class InvaildFileInput(Exception):

    """
    Can't Parse Input File
    """

    def __init__(self):
        print('Input not valid or not supported !')

class InvaidWEBVTTFile(Exception):

    """
    Can't Parse WEBVTT
    """
   
    def __init__(self):
        print("WEBVTT file is not valid!")