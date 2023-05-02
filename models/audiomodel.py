""" Audio class for handling .wav files.
"""

###########
# Imports #
###########
# Import data science packages
import numpy as np
import matplotlib.pyplot as plt

# Import system packages
import os

# Import audio packages
import soundfile as sf
import sounddevice as sd

# Import GUI packages
from tkinter import messagebox


#########
# BEGIN #
#########
class Audio:
    """ Class for use with .wav files.
    """

    def __init__(self, file_path):
        """ Read audio file and generate info.
            file_path: a Path object from pathlib
        """
        print(f"\naudiomodel: Attempting to load " + 
              f"{os.path.basename(file_path)}...")
        # Parse file path
        self.directory = os.path.split(file_path)[0]
        self.name = os.path.basename(file_path)
        self.file_path = file_path

         # Read audio file
        file_exists = os.access(self.file_path, os.F_OK)
        if not file_exists:
            print("audiomodel: Audio file not found!")
            raise FileNotFoundError
        else:
            self.signal, self.fs = sf.read(self.file_path)
            print("audiomodel: Found!")
            print(f"audiomodel: Sampling rate: {self.fs}")

        # Get number of channels
        try:
            self.num_channels = self.signal.shape[1]
        except IndexError:
            self.num_channels = 1
        self.channels = np.array(range(1, self.num_channels+1))
        print(f"audiomodel: Number of channels in file: {self.num_channels}")

        # Assign audio file attributes
        self.dur = len(self.signal) / self.fs
        self.t = np.arange(0, self.dur, 1/self.fs)
        print(f"audiomodel: Duration: {np.round(self.dur, 2)} seconds " +
            f"({np.round(self.dur/60, 2)} minutes)")

        # Get data type
        self.data_type = self.signal.dtype
        print(f"audiomodel: Data type: {self.data_type}")


    def play(self, level=None, device_id=None):
        """ Present audio
        """
        print("\naudiomodel: Preparing to present audio...")
        # Create a temporary signal to be modified
        temp = self.signal.copy()
        temp = temp.astype(np.float32)

        # Assign audio device defaults
        sd.default.device = device_id
        sd.default.samplerate = self.fs

        # Get number of available audio device channels
        try:
            self.num_outputs = sd.query_devices(sd.default.device)['max_output_channels']
        except sd.PortAudioError:
            messagebox.showerror(
                title="Invalid Audio Device",
                message="Invalid audio device!",
                detail="Please provide a valid audio device " +
                "id before continuing."
            )
            return

        # Display audio device features to console
        print(f"audiomodel: Audio device: " + 
              f"{sd.query_devices(sd.default.device)['name']}")
        print(f"audiomodel: Device outputs: {self.num_outputs}")

        # Set presentation level
        if level == None:
            # Normalize if no level is provided
            print("audiomodel: No level provided, normalizing...")
            for chan in range(0, self.num_channels):
                 # Remove DC offset
                temp[:, chan] = temp[:, chan] - np.mean(temp[:, chan])
                # Normalize
                temp[:, chan] = temp[:, chan] / np.max(np.abs(temp[:, chan]))
                # account for num channels
                temp[:, chan] = temp[:, chan] / self.num_channels 
                #print(f"\nMax of signal: {np.max(np.abs(self.signal[:, chan]))}")
                #print(f"Max of temp: {np.max(np.abs(temp[:, chan]))}")
        else:
            # Convert level in dB to magnitude
            mag = self.db2mag(level)
            # Apply scaling factor to temp
            temp = temp * mag

        print(f"audiomodel: Audio shape: {temp.shape}")

        # Check for clipping after level has been applied
        if np.max(np.abs(temp)) > 0.999:
            self._clipping(temp)

        # Present audio
        print("audiomodel: Attempting to present audio...")
        # Check that audio device has enough channels for audio
        if self.num_outputs < self.num_channels:
            print(f"\naudiomodel: {self.num_channels}-channel file, but "
                f"only {self.num_outputs} audio device output channels!")
            print("audiomodel: Dropping " +
                f"{self.num_channels - self.num_outputs} audio file channels")
            try:
                sd.play(temp[:, 0:self.num_outputs])
                #sd.wait(self.dur+0.5)
            except Exception as e:
                print(e)
            print("audiomodel: Done")
        else:
            try:
                sd.play(temp)
                #sd.wait(self.dur+0.5)
            except Exception as e:
                print(e)
            print("audiomodel: Done")


    def stop(self):
        """ Stop audio presentation.
        """
        sd.stop()


    def plot_wave(self, sig):
        plt.plot(self.t, sig)
        plt.title("Clipping Has Occurred!")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.axhline(y=1, color='red', linestyle='--')
        plt.axhline(y=-1, color='red', linestyle='--')
        plt.show()


    def _clipping(self, temp):
        messagebox.showerror(
            title="Clipping",
            message="The level provided is too high. Enter a lower level.",
            detail="The waveform will be plotted when this message is " +
                "closed for visual inspection."
        )
        self.plot_wave(temp)
        raise Exception("audiomodel: Clipping occurred")


    @staticmethod
    def db2mag(db):
        """ 
            Convert decibels to magnitude. Takes a single
            value or a list of values.
        """
        # Must use this form to handle negative db values!
        try:
            mag = [10**(x/20) for x in db]
            return mag
        except:
            mag = 10**(db/20)
            return mag


    @staticmethod
    def mag2db(mag):
        """ 
            Convert magnitude to decibels. Takes a single
            value or a list of values.
        """
        try:
            db = [20 * np.log10(x) for x in mag]
            return db
        except:
            db = 20 * np.log10(mag)
            return db


    def rms(self, sig):
        """ 
            Calculate the root mean square of a signal. 
            
            NOTE: np.square will return invalid, negative 
                results if the number excedes the bit 
                depth. In these cases, convert to int64
                EXAMPLE: sig = np.array(sig,dtype=int)

            Written by: Travis M. Moore
            Last edited: Feb. 3, 2020
        """
        theRMS = np.sqrt(np.mean(np.square(sig)))
        return theRMS


    def setRMS(self, sig, amp, eq='n'):
        """
            Set RMS level of a 1-channel or 2-channel signal.
        
            SIG: a 1-channel or 2-channel signal
            AMP: the desired amplitude to be applied to 
                each channel. Note this will be the RMS 
                per channel, not the total of both channels.
            EQ: takes 'y' or 'n'. Whether or not to equalize 
                the levels in a 2-channel signal. For example, 
                a signal with an ILD would lose the ILD with 
                EQ='y', so the default in 'n'.

            EXAMPLE: 
            Create a 2 channel signal
            [t, tone1] = mkTone(200,0.1,30,48000)
            [t, tone2] = mkTone(100,0.1,0,48000)
            combo = np.array([tone1, tone2])
            adjusted = setRMS(combo,-15)

            Written by: Travis M. Moore
            Created: Jan. 10, 2022
            Last edited: May 17, 2022
        """
        if len(sig.shape) == 1:
            rmsdb = self.mag2db(self.rms(sig))
            refdb = amp
            diffdb = np.abs(rmsdb - refdb)
            if rmsdb > refdb:
                sigAdj = sig / self.db2mag(diffdb)
            elif rmsdb < refdb:
                sigAdj = sig * self.db2mag(diffdb)
            # Edit 5/17/22
            # Added handling for when rmsdb == refdb
            elif rmsdb == refdb:
                sigAdj = sig
            return sigAdj
            
        elif len(sig.shape) == 2:
            rmsdbLeft = self.mag2db(self.rms(sig[0]))
            rmsdbRight = self.mag2db(self.rms(sig[1]))

            ILD = np.abs(rmsdbLeft - rmsdbRight) # get lvl diff

            # Determine lvl advantage
            if rmsdbLeft > rmsdbRight:
                lvlAdv = 'left'
                #print("Adv: %s" % lvlAdv)
            elif rmsdbRight > rmsdbLeft:
                lvlAdv = 'right'
                #print("Adv: %s" % lvlAdv)
            elif rmsdbLeft == rmsdbRight:
                lvlAdv = None

            #refdb = amp - 3 # apply half amp to each channel
            refdb = amp
            diffdbLeft = np.abs(rmsdbLeft - refdb)
            diffdbRight = np.abs(rmsdbRight - refdb)

            # Adjust left channel
            if rmsdbLeft > refdb:
                sigAdjLeft = sig[0] / self.db2mag(diffdbLeft)
            elif rmsdbLeft < refdb:
                sigAdjLeft = sig[0] * self.db2mag(diffdbLeft)
            # Adjust right channel
            if rmsdbRight > refdb:
                sigAdjRight = sig[1] / self.db2mag(diffdbRight)
            elif rmsdbRight < refdb:
                sigAdjRight = sig[1] * self.db2mag(diffdbRight)

            # If there is a lvl difference to maintain across channels
            if eq == 'n':
                if lvlAdv == 'left':
                    sigAdjLeft = sigAdjLeft * self.db2mag(ILD/2)
                    sigAdjRight = sigAdjRight / self.db2mag(ILD/2)
                elif lvlAdv == 'right':
                    sigAdjLeft = sigAdjLeft / self.db2mag(ILD/2)
                    sigAdjRight = sigAdjRight * self.db2mag(ILD/2)

            sigBothAdj = np.array([sigAdjLeft, sigAdjRight])
            return sigBothAdj
