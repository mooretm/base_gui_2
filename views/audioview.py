""" Audio dialog
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import data science packages
import numpy as np
import pandas as pd
from pandastable import Table

# Import audio packages
import sounddevice as sd


#########
# BEGIN #
#########
class AudioDialog(tk.Toplevel):
    """ Audio device dialog.
    """
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, *kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        # Window setup
        self.withdraw()
        self.focus()
        self.title("Audio")
        self.grab_set() # Disable root window (toplevel as modal window)

        # Draw widgets
        self._draw_widgets()

        # Show device table
        self._show_audio_devices()

        # Center calibration window dialog
        self.center_window()


    def _draw_widgets(self):
        ##########
        # Frames #
        ##########
        # Options for label frames
        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}

        # Audio device
        lfrm_settings = ttk.Labelframe(self, text='Audio Device')
        lfrm_settings.grid(column=0, row=0, sticky='nsew', **options)

        # Audio device table
        self.frmTable = ttk.Frame(self)
        self.frmTable.grid(column=0, row=15, **options)


        ###########
        # Widgets #
        ###########
        # Audio device ID
        ttk.Label(lfrm_settings, text="Audio Device ID:").grid(
            column= 5, row=10, sticky='e', **options_small)
        ent_deviceID = ttk.Entry(lfrm_settings, 
            textvariable=self.sessionpars['audio_device'], width=6)
        ent_deviceID.grid(column=10, row=10, sticky='w', **options_small)

        # Submit button
        btnDeviceID = ttk.Button(self, text="Submit", 
            command=self._on_submit)
        btnDeviceID.grid(column=0, columnspan=10, row=10, **options_small)

        # Speaker number
        # lbl_speaker = ttk.Label(lfrm_settings, text='Output Speaker:').grid(
        #     column=5, row=5, sticky='e', **options_small)
        # ent_speaker = ttk.Entry(lfrm_settings, 
        #     textvariable=self.sessionpars['Speaker Number'], width=6)
        # ent_speaker.grid(column=10, row=5, sticky='w', **options_small)


    #################
    # General Funcs #
    #################
    def center_window(self):
        """ Center the root window 
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _show_audio_devices(self):
        # Get and display list of audio devices
        deviceList = sd.query_devices()
        print("\naudioview: Audio Devcie List")
        print(deviceList)
        
        names = [deviceList[x]['name'] for x in np.arange(0,len(deviceList))]
        chans_out =  [deviceList[x]['max_output_channels'] for x in np.arange(0,len(deviceList))]
        ids = np.arange(0,len(deviceList))
        df = pd.DataFrame({
            "device_id": ids, 
            "name": names, 
            "chans_out": chans_out})
        pt = Table(self.frmTable, dataframe=df, showtoolbar=True, showstatusbar=True)
        table = pt = Table(self.frmTable, dataframe=df)
        table.grid(column=0, row=0)
        pt.show()
    

    def _on_submit(self):
        print("\nView_Audio_99: Sending save audio config event...")
        self.parent.event_generate('<<AudioDialogSubmit>>')
        self.destroy()
