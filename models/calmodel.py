""" Class for loading calibration file, determining calibration 
    offset, and calculating presentation level.

    Written by: Travis M. Moore
"""

############
# IMPORTS  #
############
# Import system packages
import os

# Import custom modules
from models import audiomodel
from functions import resource_path


#########
# MODEL #
#########
class CalModel:
    """ Write provided dictionary to .csv
    """
    def __init__(self, sessionpars):
        self.sessionpars = sessionpars


    def _get_cal_file(self):
        """ Load specified calibration file
        """
        print("calmodel: Locating calibration file...")
        if self.sessionpars['cal_file'].get() == 'cal_stim.wav':
            self.cal_file = resource_path.resource_path('cal_stim.wav')
            #self.cal_file = self.resource_path('cal_stim.wav')
            file_exists = os.access(self.cal_file, os.F_OK)
            if not file_exists:
                self.cal_file = '.\\assets\\cal_stim.wav'
        else: # Custom file was provided
            self.cal_file = self.sessionpars['cal_file'].get()

        print(f"calmodel: Using {self.cal_file}")


    def _calc_level(self):
        """ Calculate and save adjusted presentation level
        """
        # Calculate SLM offset
        print("\ncalmodel: Calculating new presentation level...")
        slm_offset = self.sessionpars['slm_reading'].get() - self.sessionpars['scaling_factor'].get()
        # Provide console feedback
        print(f"calmodel: Starting level (dB FS): " +
              f"{self.sessionpars['scaling_factor'].get()}")
        print(f"calmodel: SLM reading (dB): " +
              f"{self.sessionpars['slm_reading'].get()}")
        print(f"calmodel: SLM offset: {slm_offset}")

        # Calculate new presentation level
        self.sessionpars['adj_pres_level'].set(
            self.sessionpars['pres_level'].get() - slm_offset)
        print(f"calmodel: Desired level (dB): " +
              f"{self.sessionpars['pres_level'].get()}")
        print(f"calmodel: New presentation level: " +
            f"{self.sessionpars['adj_pres_level'].get()}")

        # Save SLM offset and updated level
        #self.app._save_sessionpars()
        # This must happen in controller...


    def play_cal(self):
        # Present calibration file
        self.cal = audiomodel.Audio(file_path=self.cal_file)
        self.cal.play(
            level=self.sessionpars['scaling_factor'].get(),
            device_id=self.sessionpars['audio_device'].get()
        )

    
    def stop_cal(self):
        try:
            self.cal.stop()
        except AttributeError:
            print("calmodel: No calibration stimulus found!")
