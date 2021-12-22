class InvaildFileInput(Exception):

    """
    Can't Parse Input File
    """

    def __init__(self):
        print('Input not valid or not supported !')

    def __str__(self) -> str: return 'Input not valid or not supported !'

class InvaidWEBVTTFile(Exception):

    """
    Can't Parse WEBVTT
    """
   
    def __init__(self):
        print("WEBVTT file is not valid!")

    def __str__(self) -> str: return "WEBVTT file is not valid!"