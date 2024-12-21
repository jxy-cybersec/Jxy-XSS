import os
import platform

def supports_ansi():
    if os.name == "nt" and platform.system() != "Windows-10":
        return False
    return True

if supports_ansi():
    white = '\033[97m'
    green = '\033[92m'
    red = '\033[91m'
    yellow = '\033[93m'
    end = '\033[0m'
else:
    white = green = red = yellow = end = ''
