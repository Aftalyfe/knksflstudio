# name=KORG nanoKONTROL Studio

import playlist
import channels
import mixer
import patterns
import arrangement
import ui
import transport
import device
import general
import launchMapPages
import midi

# don't change these!!!!
MODE1 = "f042400001370200004f00f7"
MODE2 = "f042400001370200004f01f7"
MODE3 = "f042400001370200004f02f7"
MODE4 = "f042400001370200004f03f7"
MODE5 = "f042400001370200004f04f7"

# when moving a fader show mixer automatically
AUTO_SWITCH_TO_CONTROLLED_PARAMETER = True

# set these to whatever tracks you want to control in a particular group on your mixer
FADER1a = 0
FADER2a = 104
FADER3a = 105
FADER4a = 106
FADER5a = 100
FADER6a = 101
FADER7a = 102
FADER8a = 103
# 2nd group
FADER1b = 1
FADER2b = 2
FADER3b = 3
FADER4b = 4
FADER5b = 5
FADER6b = 6
FADER7b = 7
FADER8b = 8
# 3rd group
FADER1c = 9
FADER2c = 10
FADER3c = 11
FADER4c = 12
FADER5c = 13
FADER6c = 14
FADER7c = 15
FADER8c = 16
# 4th group
FADER1d = 17
FADER2d = 18
FADER3d = 19
FADER4d = 20
FADER5d = 21
FADER6d = 22
FADER7d = 23
FADER8d = 24
# 5th group
FADER1e = 25
FADER2e = 26
FADER3e = 27
FADER4e = 28
FADER5e = 29
FADER6e = 30
FADER7e = 31
FADER8e = 32
# 6th group
FADER1f = 33
FADER2f = 34
FADER3f = 35
FADER4f = 36
FADER5f = 37
FADER6f = 38
FADER7f = 39
FADER8f = 40
# 7th group
FADER1g = 41
FADER2g = 42
FADER3g = 43
FADER4g = 44
FADER5g = 45
FADER6g = 46
FADER7g = 47
FADER8g = 48
# 8th group
FADER1h = 49
FADER2h = 50
FADER3h = 51
FADER4h = 52
FADER5h = 53
FADER6h = 54
FADER7h = 55
FADER8h = 56


# status - 144 = note on, 128 = note off, 177 = control change, 240 = system messages
# data1 - cc number
# data2 - cc value

# device.midiOutMsg(event.midiId, event.midiChan, event.data1, event.data2) <- format to trigger controller LEDs

# The LEDs light up or go off when a message with the control change number
# or note number assigned to a button is received from the computer. When an
# On Value or note-on message is received, the LED lights up. When an Off Value
# or note-off message is received, the LED turns off

class Controller:
    def __init__(self):
        self.current_mode = 1  # what is the current scene on the controller
        self.current_fader_group = 0  # what group of faders is currently active
        self.shifting = 0 # is shift (cycle) button pressed
        self.switch_window = AUTO_SWITCH_TO_CONTROLLED_PARAMETER  # is mixer shown automatically when moving faders
        self.fader_map = [  # this is a map of 8 fader sets in fl studio,
            # customize the constants at the top to control tracks of your choice)
            # to understand how this works, look up 2D lists in python
            [FADER1a, FADER2a, FADER3a, FADER4a, FADER5a, FADER6a, FADER7a, FADER8a],
            [FADER1b, FADER2b, FADER3b, FADER4b, FADER5b, FADER6b, FADER7b, FADER8b],
            [FADER1c, FADER2c, FADER3c, FADER4c, FADER5c, FADER6c, FADER7c, FADER8c],
            [FADER1d, FADER2d, FADER3d, FADER4d, FADER5d, FADER6d, FADER7d, FADER8d],
            [FADER1e, FADER2e, FADER3e, FADER4e, FADER5e, FADER6e, FADER7e, FADER8e],
            [FADER1f, FADER2f, FADER3f, FADER4f, FADER5f, FADER6f, FADER7f, FADER8f],
            [FADER1g, FADER2g, FADER3g, FADER4g, FADER5g, FADER6g, FADER7g, FADER8g],
            [FADER1h, FADER2h, FADER3h, FADER4h, FADER5h, FADER6h, FADER7h, FADER8h]
        ]

    def update_mode(self, mode):  # when scene needs to be switched
        if mode == MODE1:
            self.current_mode = 1
        elif mode == MODE2:
            self.current_mode = 2
        elif mode == MODE3:
            self.current_mode = 3
        elif mode == MODE4:
            self.current_mode = 4
        else:
            self.current_mode = 5

    def light_up(self, midi_channel):  # initial turning on the LED's
        device.midiOutMsg(176, midi_channel, 54, 127)
        device.midiOutMsg(176, midi_channel, 55, 127)
        device.midiOutMsg(176, midi_channel, 56, 127)
        device.midiOutMsg(176, midi_channel, 57, 127)
        device.midiOutMsg(176, midi_channel, 58, 127)
        device.midiOutMsg(176, midi_channel, 59, 127)
        device.midiOutMsg(176, midi_channel, 60, 127)
        device.midiOutMsg(176, midi_channel, 61, 127)
        device.midiOutMsg(176, midi_channel, 62, 127)
        device.midiOutMsg(176, midi_channel, 63, 127)
        for group in range(0, 7):
            device.midiOutMsg(176, midi_channel, 47 + group, 0)
        device.midiOutMsg(176, midi_channel, 46, 127)

    def update_fader_group(self, data):  # when another fader group is selected
        if self.current_fader_group != 0 and data == 60:
            self.current_fader_group = self.current_fader_group - 1
            #print(self.current_fader_group)
            return
        elif self.current_fader_group == 0 and data == 60:
            #print(self.current_fader_group)
            return
        elif self.current_fader_group != 7 and data == 61:
            self.current_fader_group = self.current_fader_group + 1
            #print(self.current_fader_group)
            return
        elif self.current_fader_group == 7 and data == 61:
            #print(self.current_fader_group)
            return
        else:
            self.current_fader_group = data - 46

    def update_switch_window(self, data):
        self.switch_window = data


controller = Controller()


def OnInit():  # these lines turn on the button LEDs on the controller
    controller.light_up(0)


def hex_it(sysex):  # turns whatever is given to hexadecimal number, if it's not something you can turn, returns none
    if sysex:
        return sysex.hex()
    else:
        return "None"


def print_midi_info(event):  # quick code to see info about particular midi control (check format function in python)
    print("handled: {}, timestamp: {}, status: {}, data1: {}, data2: {}, port: {}, sysex: {}, midiId: {}".format(
        event.handled, event.timestamp, event.status, event.data1, event.data2, event.port, hex_it(event.sysex),
        event.midiId))


def OnMidiIn(event):  # this executes for every MIDI input from the controller
    #print_midi_info(event)
    if event.data1 == 54: # turn on shifting so the buttons can do alternate things
        if event.data2 == 127:
            controller.shifting = 1
            #print(controller.shifting)
        else:
            controller.shifting = 0
            #print(controller.shifting)


# print(event.midiId, event.midiChan)
# print(mixer.getTrackInfo(2))

def OnMidiMsg(event):  # same as above, but executes after OnMidiIn
    return


def OnSysEx(event):  # executes only when pressing "Scene" as that is the only sysex event
    controller.update_mode(hex_it(event.sysex))
    controller.light_up(event.midiChan)


# print("The current mode is: " + str(controller.current_mode))

# ---------------------------------------------------------------------------------------------------------------------
# MAIN SECTION CODE
# ---------------------------------------------------------------------------------------------------------------------

def OnControlChange(event):
    # executes when there is a control change as opposed to a note change
    # (for this controller basically everything executes from here)
    if event.data1 == 80:  # play button
        transport.start()
        if transport.isPlaying():
            device.midiOutMsg(event.midiId, event.midiChan, 80, 127)
        elif transport.isPlaying() == False:
            device.midiOutMsg(event.midiId, event.midiChan, 80, 0)
        # print(event.midiChan)
        # print(type(event.midiChan))
        event.handled = True
        return
    if event.data1 == 63:  # stop button
        if transport.isPlaying():
            device.midiOutMsg(event.midiId, event.midiChan, 80, 0)
        # print(event.midiId)
        transport.stop()
        event.handled = True
        return
    if event.data1 == 83:  # jog wheel transport
        transport.setSongPos(transport.getSongPos() + (event.data2 / 200))
        event.handled = True
    if event.data1 == 85:  # jog wheel transport
        if transport.getSongPos() > 0:  # if this condition is not here jog wheel goes into countdown
            target_position = transport.getSongPos() - (event.data2 / 200)
            if target_position > 0:
                transport.setSongPos(target_position)
            else:
                transport.setSongPos(0)
        event.handled = True
    if event.data1 == 62:  # restart the song
        transport.setSongPos(0)
        event.handled = True
    if event.data1 == 81:  # toggles recording on and off
        transport.record()
        if transport.isRecording():
            device.midiOutMsg(event.midiId, 0, 81, 127)
        else:
            device.midiOutMsg(event.midiId, 0, 81, 0)
        event.handled = True
    if event.data1 == 58 and event.data2 == 127:  # toggles rewind on and off
        transport.rewind(2)
        event.handled = True
    elif event.data1 == 58 and event.data2 == 0:
        transport.rewind(0)
        event.handled = True
    if event.data1 == 59 and event.data2 == 127:  # toggles fast forward on and off
        transport.fastForward(2)
        event.handled = True
    elif event.data1 == 59 and event.data2 == 0:
        transport.fastForward(0)
        event.handled = True
    if event.data1 == 57:
        transport.markerJumpJog(1)
        event.handled = True
    if event.data1 == 56:
        transport.markerJumpJog(-1)
        event.handled = True
    if event.data1 == 55:
        transport.globalTransport(106, 1)
        event.handled = True
    # ---------------------------------------------------------------------------------------------------------------------
    # FADER GROUPS CODE
    # ---------------------------------------------------------------------------------------------------------------------
    # if current scene is the first one make faders control mixer, otherwise assign them yourself
    if controller.current_mode == 1:
        # switch the current fader group one up or down
        if event.data1 == 60 or event.data1 == 61:
            controller.update_fader_group(event.data1)
            if event.data1 == 60:
                device.midiOutMsg(176, event.midiChan, controller.current_fader_group + 47, 0)  # LED button off
            else:
                device.midiOutMsg(176, event.midiChan, controller.current_fader_group + 46, 127)  # LED button on
            for track in range(21, 46):  # turn all mute, solo and arm LEDs off
                if track != 32:
                    device.midiOutMsg(176, event.midiChan, track, 0)
            # turn all mute, solo and arm LEDs on that should be on
            for num, item in enumerate(controller.fader_map[controller.current_fader_group]):
                if mixer.isTrackSolo(item):
                    if 0 <= num <= 2:  # because there is no button with cc 32
                        device.midiOutMsg(176, event.midiChan, num + 29, 127)
                    else:
                        device.midiOutMsg(176, event.midiChan, num + 30, 127)
                if mixer.isTrackArmed(item):
                    device.midiOutMsg(176, event.midiChan, num + 38, 127)
                if mixer.isTrackMuted(item):
                    device.midiOutMsg(176, event.midiChan, num + 21, 127)
            event.handled = True
        # when any fader is moved, moves the volume fader in FL studio according to what is set in the constants at the beginning
        if 91 <= event.data1 <= 98:
            mixer.setTrackVolume(controller.fader_map[controller.current_fader_group][event.data1 - 91],
                                 (event.data2 / 127) * 0.8)
            if controller.switch_window:  # show mixer when faders move if its set so at the beginning
                ui.showWindow(0)
                ui.setFocused(0)
            # print("Current fader group is: " + str(controller.current_fader_group))
            event.handled = True
        # also switches the current fader group, but via the select buttons
        if 46 <= event.data1 <= 53:  # if select buttons are pressed
            controller.update_fader_group(event.data1)  # set fader group to one of 8
            for track in range(21, 46):  # turn all mute, solo and arm LEDs off
                if track != 32:
                    device.midiOutMsg(176, event.midiChan, track, 0)  #
            for num, item in enumerate(
                    controller.fader_map[controller.current_fader_group]):  # turn on all LEDs that should be on
                if mixer.isTrackSolo(item):
                    if 0 <= num <= 2:
                        device.midiOutMsg(176, event.midiChan, num + 29, 127)
                    else:
                        device.midiOutMsg(176, event.midiChan, num + 30, 127)
                if mixer.isTrackArmed(item):
                    device.midiOutMsg(176, event.midiChan, num + 38, 127)
                if mixer.isTrackMuted(item):
                    device.midiOutMsg(176, event.midiChan, num + 21, 127)
            for group in range(46, event.data1 + 1):  # turn on and off select LEDs
                device.midiOutMsg(176, event.midiChan, group, 127)
            for group in range(event.data1 + 1, 54):
                device.midiOutMsg(176, event.midiChan, group, 0)
            # print("Current fader group is: " + str(controller.current_fader_group))
            event.handled = True
        # arms and disarms track for recording
        if 38 <= event.data1 <= 45:
            mixer.armTrack(controller.fader_map[controller.current_fader_group][event.data1 - 38])
            if mixer.isTrackArmed(controller.fader_map[controller.current_fader_group][event.data1 - 38]):
                # turns on REC LEDs
                device.midiOutMsg(176, event.midiChan, event.data1, 127)
            else:
                device.midiOutMsg(176, event.midiChan, event.data1, 0)
            event.handled = True
        # solo and unsolo tracks for the first three buttons (because the 4th solo button does not have value 32)
        if 29 <= event.data1 <= 31:
            mixer.soloTrack(controller.fader_map[controller.current_fader_group][event.data1 - 29])
            if mixer.isTrackSolo(controller.fader_map[controller.current_fader_group][event.data1 - 29]):
                for track in range(29, 38):
                    if track != 32:
                        device.midiOutMsg(176, event.midiChan, track, 0)
                device.midiOutMsg(176, event.midiChan, event.data1, 127)
                # also turns on MUTE LEDs for the channels that are muted due to solo
                for track in range(21, 29):
                    if event.data1 != (track + 8):
                        device.midiOutMsg(176, event.midiChan, track, 127)
                    else:
                        device.midiOutMsg(176, event.midiChan, track, 0)
            else:
                device.midiOutMsg(176, event.midiChan, event.data1, 0)
                for num in range(0, 8):
                    device.midiOutMsg(176, event.midiChan, num + 21, 0)
            event.handled = True
        # solo and unsolo tracks for the other 5 buttons (because the 4th solo button does not have value 32)
        if 33 <= event.data1 <= 37:
            mixer.soloTrack(
                controller.fader_map[controller.current_fader_group][event.data1 - 30])  # solos the mixer track
            if mixer.isTrackSolo(controller.fader_map[controller.current_fader_group][
                                     event.data1 - 30]):  # checks to see if the track is soloed
                for track in range(29, 38):
                    if track != 32:
                        device.midiOutMsg(176, event.midiChan, track, 0)
                device.midiOutMsg(176, event.midiChan, event.data1, 127)
                for track in range(21, 29):
                    if event.data1 != (track + 9):
                        device.midiOutMsg(176, event.midiChan, track, 127)
                    else:
                        device.midiOutMsg(176, event.midiChan, track, 0)
            else:
                device.midiOutMsg(176, event.midiChan, event.data1, 0)
                for num in range(0, 8):
                    device.midiOutMsg(176, event.midiChan, num + 21, 0)
            event.handled = True
        # mute and unmute mixer tracks
        if 21 <= event.data1 <= 28:
            if mixer.isTrackEnabled(controller.fader_map[controller.current_fader_group][event.data1 - 21]):
                device.midiOutMsg(176, event.midiChan, event.data1, 127)
            else:
                device.midiOutMsg(176, event.midiChan, event.data1, 0)
            mixer.enableTrack(controller.fader_map[controller.current_fader_group][event.data1 - 21])
            event.handled = True
        if 13 <= event.data1 <= 20:
            if controller.shifting == 0:
                if 55 <= event.data2 <= 70: #snaps the pan to 0 when it's close to center
                    mixer.setTrackPan((controller.fader_map[controller.current_fader_group][event.data1 - 13]), 0)
                else:
                    mixer.setTrackPan((controller.fader_map[controller.current_fader_group][event.data1 - 13]), (event.data2 - 63.5)/63.5)
            else:
                if 55 <= event.data2 <= 70:
                    #midi.REC_Mixer_SS + mixer.getTrackPluginId(controller.fader_map[controller.current_fader_group][event.data1 - 13], 0)
                    print(mixer.getTrackPluginId(controller.fader_map[controller.current_fader_group][event.data1 - 13], midi.REC_Mixer_SS))
                else:
                    #midi.REC_Mixer_SS + mixer.getTrackPluginId(controller.fader_map[controller.current_fader_group][event.data1 - 13], (event.data2 - 63.5)/63.5)
                    print(mixer.getTrackPluginId(controller.fader_map[controller.current_fader_group][event.data1 - 13], midi.REC_Mixer_SS))
            event.handled = True