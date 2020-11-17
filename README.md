# knksflstudio
Script for Korg nanoKONTROL Studio controller for FL Studio

Key features:

- jog wheel scrolls through the project
- play, rec, stop, restart, rewind, ff buttons
- 8 groups of 8 faders controlling 64 tracks altogether which can be selected either by track < and > buttons or by pressing any of the 8 "select" buttons which in turn will select the corresponding group of mixer tracks to control (you can specify your own tracks you want to control inside the script)
- first group consists of master track, 3 bus tracks, 3 send tracks and a recording track, other groups control regular mixer tracks from 1 to 58
- pan, volume, mute, solo, arm buttons work as expected with faders snapping the max volume to 0db and panning snapping to zero as well
- the script consisting of 3 files: the script itself, the korg editor file and an fl studio template (which is optional but recommended)
- 5 "scenes" where the first scene is predefined as controlling the mixer, all other scenes are assignable the usual way
- "cycle" button is doing the function of a "shift" button and will be used in later versions to add more functionality
- "set" button is essentially a "tap tempo" button
- skip to next and previous marker buttons
- moving a fader displays the mixer right away (can be turned off via a constant if necessary)

HOW TO INSTALL:

1. Make sure to put the provided .py file in a "KORG nanoKontrol Studio" folder in the C:\Users\(your name)\Documents\Image-Line\FL Studio\Settings\Hardware
2. Make sure to have installed and open KORG Kontrol Editor and open the "AftaKNKSFLStudio.nktrl_st_set" file provided inside it. After you opened it you need to "write" it to the controller by going to Communication > Write Scene Set. You should get a warning message, just click confirm.
3. (optional) Make sure to put the FL Studio Template file inside "C:\Program Files (x86)\Image-Line\FL Studio 20\Data\Templates"
4. Open FL Studio and go to Options > MIDI Settings. Find your device in the list and assign a script to it the usual way. Next open the FL studio template provided as it's going to make a lot more sense as to what tracks are controlled with what fader in the first group.

There is a probability that your controller will not be recognized by Windows, i.e. it will not appear in the list of controllers in FL Studio even though it is connected to the computer. If that happens you need to download drivers from the KORG webpage. Before installing those drivers make sure to go into registry editor and navigate to this folder "Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Drivers32". Once in there delete all "midix" files with a number (where x is a number, dont worry they will auto generate again). Immediately after that run the driver installation. After the driver is installed go back to the registry editor, the midi files will be back, check that one of those midi files data says: KORGUM64.DRV. This will mean that the drivers have been successfully installed.

This script should work with all versions of FL Studio starting from the version 20.7.2. You can change what mixer tracks are controlled by changing the constant numbers at the start of the script.

I included small hints inside the script to explain what everything does, if you have any questions feel free to ask.

PLANNED UPDATES:
- while "cycle" is pressed panning knobs controls stereo separation of a track

