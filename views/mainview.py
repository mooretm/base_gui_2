""" Main view for Vesta
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets
        """
        ##########
        # Styles #
        ##########
        style = ttk.Style()


        #################
        # Create frames #
        #################
        options = {'padx':10, 'pady':10}

        # Main container
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, **options)

        ##################
        # Create Widgets #
        ##################
        lbl_label1 = ttk.Label(frm_main, text="Base GUI")
        lbl_label1.grid(row=0, column=0)

        btn_save = ttk.Button(frm_main, text="Save", command=self._on_save)
        btn_save.grid()


    #############
    # Functions #
    #############
    def _on_save(self):
        self.event_generate('<<MainSave>>')
