""" Audio device selection view
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

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
        self.title("Audio Device Selection")
        self.grab_set() # Disable root window (toplevel as modal window)

        # Draw widgets
        self._draw_widgets()

        # Center calibration window dialog
        self.center_window()


    def _draw_widgets(self):
        ##########
        # Frames #
        ##########
        # Options for label frames
        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}

        # Audio device table
        self.frm_tree = ttk.Frame(self)
        self.frm_tree.grid(column=5, row=5, **options)

        # Submit button
        frm_submit = ttk.Frame(self)
        frm_submit.grid(column=5, row=10, **options)

        ###########
        # Widgets #
        ###########
        # Create treeview
        self.tree = self._create_tree_widget()

        # Submit button
        ttk.Button(frm_submit, text="Submit", command=self._on_submit).grid(
            column=5, columnspan=15, row=5)
        

    def _create_tree_widget(self):
        """ Create and populate treeview.
        """
        columns = ('device_id', 'device_name', 'channels_out')
        tree = ttk.Treeview(self.frm_tree, columns=columns, show='headings')

        # Define headings
        tree.heading('device_id', text='Device ID')
        tree.heading('device_name', text='Device Name')
        tree.heading('channels_out', text='Outputs')

        # Define columns
        tree.column('device_id', width=60, anchor=tk.CENTER)
        tree.column('device_name', width=400, anchor=tk.W)
        tree.column('channels_out', width=60, anchor=tk.CENTER)

        tree.bind('<<TreeviewSelect>>', self._item_selected)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.frm_tree, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Get data
        devices = self._query_audio_devices()

        # Populate tree
        for device in devices:
            tree.insert('', tk.END, values=device)

        return tree


    def _query_audio_devices(self):
        """ Create list of tuples with specified device information.
        """
        # Get list of audio devices
        deviceList = sd.query_devices()
        print("\naudioview: Audio Devcie List")
        print(deviceList)
        
        # Create list of tuples with device info
        devices = []
        for ii in range(0,len(deviceList)):
            if deviceList[ii]['max_output_channels'] > 0:
                devices.append((ii, deviceList[ii]['name'], deviceList[ii]['max_output_channels']))

        return devices


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


    def _item_selected(self, event):
        """ Update audio device ID with the device selected
            from the tree.
        """
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']

            # Update sessionpars with device id
            self.sessionpars['audio_device'].set(record[0])


    def _on_submit(self):
        """ Send submit event to controller.
        """
        print("\naudioview: Sending save audio device event...")
        self.parent.event_generate('<<AudioDialogSubmit>>')
        self.destroy()
