""" Model for storing session parameters 
"""

############
# IMPORTS  #
############
# Import system packages
from pathlib import Path

# Import data handling packages
import json
from glob import glob


#########
# BEGIN #
#########
class SessionParsModel:
    # Define dictionary items
    fields = {
        'subject': {'type': 'str', 'value': '999'},
        'condition': {'type': 'str', 'value': 'TEST'},
        'pres_level': {'type': 'float', 'value': 65},
        'randomize': {'type': 'int', 'value': 0},
        'repetitions': {'type': 'int', 'value': 1},
        #'Speaker Number': {'type': 'int', 'value': 1},
        'audio_files_path': {'type': 'str', 'value': 'Please select a folder'},
        'matrix_file_path': {'type': 'str', 'value': 'Please select a file'},
        'audio_device': {'type': 'int', 'value': 999},
        'raw_lvl': {'type': 'float', 'value': -30},
        'slm_reading': {'type': 'float', 'value': 70},
        'adj_pres_level': {'type': 'float', 'value': -30},
        'scaling_factor': {'type': 'float', 'value': -30},
        'cal_file': {'type': 'str', 'value': 'cal_stim.wav'}
    }

    def __init__(self):
        # Create session parameters file
        filename = 'base_gui2.json'

        # Store settings file in user's home directory
        self.filepath = Path.home() / filename

        # Load settings file
        self.load()


    def load(self):
        """ Load session parameters from file
        """
        # If the file doesn't exist, abort
        print("\nsessionmodel: Checking for parameter file...")
        if not self.filepath.exists():
            return

        # Open the file and read in the raw values
        print("sessionmodel: File found - reading raw values from " +
            "parameter file...")
        with open(self.filepath, 'r') as fh:
            raw_values = json.load(fh)

        # Don't implicitly trust the raw values: only get known keys
        print("sessionmodel: Loading vals into sessionpars model " +
            "if they match model keys")
        # Populate session parameter dictionary
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value


    def save(self):
        """ Save current session parameters to file 
        """
        # Write to JSON file
        print("sessionmodel: Writing session pars from model to file...")
        with open(self.filepath, 'w') as fh:
            json.dump(self.fields, fh)


    def set(self, key, value):
        """ Set a variable value.
        """
        print("sessionmodel: Setting sessionpars model " +
            "fields with running vals...")
        if (
            key in self.fields and 
            type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("sessionmodel: Bad key or wrong variable type")
