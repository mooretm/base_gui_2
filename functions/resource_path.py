""" Global functions.
"""

###########
# Imports #
###########
# Import system packages
import sys
import os


#########
# Funcs #
#########
def resource_path(relative_path):
    """ Create the absolute path to compiled resources
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
