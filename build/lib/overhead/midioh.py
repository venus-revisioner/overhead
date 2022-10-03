import contextlib
import random
import threading
import time

import numpy as np
# from pyo import   # only works with python >=3.8


def column_formatter(x, width=12, verbose=0):
    b = lambda y: f'{y:{width}}\t\t'
    c = list(map(b, x))
    s = "".join(c)
    s = s.strip("\t")
    if verbose:
        print(s)
    else:
        return s


class MidiNoteThread(threading.Thread):

    def __init__(self, midi_data, server):
        threading.Thread.__init__(self)
        self.midi_data = midi_data
        self.server = server

    def run(self):
        self.on(self.midi_data[0], self.midi_data[1])
        time.sleep(self.midi_data[2])
        self.off(self.midi_data[0])
        self.status()

    def status(self):
        return self.is_alive()

    def on(self, p, v):
        self.server.noteout(p, v)
    def off(self, p):
        self.server.noteout(p, 0)


class MidiNote:
    """ MidiNote class for fast and simple access to threaded midi_tools note generation.
    Use:
    m = MidiNote(device='loopMIDI', verbose=1)
    m.play((60, 100, 6, 1.))
    m.play((67, 100, 5))
    (or m.test_arpeggio() or m.demo()
    """
    def __init__(self, input_device="", output_device="", midi_data=(60, 100, 1), verbose=0):

        self.server = Server(duplex=0)
        self.server.getMidiActive()
        self.verbose = verbose

        input_devices = pm_get_input_devices()
        self.input_devices = list(zip(*input_devices))
        self.input_device_index = None
        self.input_device = input_device

        if self.input_device:
            print("Found these MIDI inputs:")
            for item in self.input_devices:
                print(item)
            self.use_input_device()

        # print("Use function 'use_input_device' to start receiving MIDI.\n")

        output_devices = pm_get_output_devices()
        self.output_devices = dict(zip(*output_devices))
        self.output_device_index = None
        self.output_device = output_device

        if self.output_device:
            print("Found these MIDI outputs:")
            for k,v in self.output_devices.items():
                print(k, v)
            time.sleep(2)
            self.use_output_device()

        # print("Use function 'use_output_device' to start sending MIDI.\n")

        self.midi_data = midi_data
        self.column_labels = ["NOTE", "VELOCITY", "LENGTH", "IOI"]

    def start_server(self):
        self.server.boot()
        self.server.start()

    def listen_midi_input(self):
    #     x, y, z = 0, 0, 0
    #     def ctl_scan2(ctlnum, midichnl):
    #         global x, y
    #         print(f'CtlScan2 -- MIDI channel: {midichnl} controller number: {ctlnum}')
    #         x, y = midichnl, ctlnum
    #         m = Midictl(ctlnumber=ctlnum, channel=midichnl)
    #         print(m.ctlnumber, m.channel)

        def raw_midi2(status, cntr, val):
            # global z
            print(f'RawMidi -- status: {status} controller: {cntr} value: {val}')
            # z = val
            # return status, cntr, val

        # ctr = CtlScan2(ctl_scan2, toprint=False)
        raw = RawMidi(raw_midi2)

        # m = Midictl(ctlnumber=ctlnum, channel=midichnl)

        self.server.gui(locals())

    def use_input_device(self, device=None):
        if device is None:
             device = self.input_device
        for i in self.input_devices:
            x, y = i
            print("I am input", x, "-- port", y)
            if device == x:
                self.input_device_index = y
                print("MATCH:", device, self.input_device_index )

                print(f'Found {device} at index {self.input_device_index}.')
                time.sleep(2)
                self.server.setMidiInputDevice(self.input_device_index)
                # pm_count_devices()
                self.start_server()
                self.listen_midi_input()
                break

    def use_output_device(self, device=None):
        if device is None:
             device = self.output_device

        # for i in self.output_devices:
        #     x, y = i
        #     if device in x:
        self.output_device_index = self.output_devices[device]

        print(f'\nFound {device} at index {self.output_device_index}\n')
        time.sleep(2)
        self.server.setMidiOutputDevice(self.output_device_index)
        # pm_count_devices()
        self.start_server()

    def map_midi(self, x, mode="piano"):
        if mode == 'piano':
            return int(x * 87 + 21)
        if mode == 'velocity':
            return int(round(x * 106 + 21, 0))
        if mode == 'max_range':
            return int(x * 127)
        if mode == 'normalize':
            return x / 127

    def play(self, midi_list):
        if midi_list[0] <= 1.0:
            midi_list[0] = self.map_midi(midi_list[0], mode="piano")
        if midi_list[1] <= 1.0:
            midi_list[1] = self.map_midi(midi_list[1], mode="velocity")
        if len(midi_list) == 3:
            self.output_midi(midi_list)
            if self.verbose:
                self.print_midi_data(midi_list)
        if len(midi_list) == 4:
            self.output_midi(midi_list[:3])
            if self.verbose:
                self.print_midi_data(midi_list)
            time.sleep(midi_list[3])

    def output_midi(self, midi_data=(60, 100, 1)):
        if not midi_data:
            midi_data = self.midi_data
        self.midi_note(midi_data)

    def midi_note(self, list):
        th = MidiNoteThread(list, self.server)
        th.start()

    def quit(self):
        self.server.stop()
        self.server.shutdown()
        exit()

    def list_devices(self):
        print(self.output_devices)

    def print_midi_data(self, midi_data, verbose=1):
        print_data = ""
        if not midi_data:
            midi_data = self.midi_data
        if len(midi_data) == 3:
            self.column_labels = self.column_labels[:3]
            print_data = [f'{self.column_labels[i]}: {[midi_data][i]}' for i in range(3)]
        if len(midi_data) == 4:
            print_data = [f'{self.column_labels[i]}: {midi_data[i]}' for i in range(4)]
        column_formatter(print_data, verbose=verbose)

    def demo(self, note_amt=100):

        scaled_range = [(1.-(i/note_amt) ** 1.4) * note_amt for i in range(note_amt)[::-1]]

        for i in range(note_amt):
            # interval = 7
            # interval = random.choice([-7, 7])
            interval = random.choice([-1, -2, 7])
            # interval = random.choice([-12, -7, 5, 10, 15])
            # interval = random.choice([2, 4, 6, 9, 11])
            # interval = random.choice([-4, 7])
            # interval = random.randint(0, 1) * 2 + 5
            # interval = random.choice([4, 7])
            # interval = random.choice([-2, 7])
            # interval = random.randint(-1, 1) * 2 + 5
            # interval = random.randint(0, 1) * 14 - 7

            pitch = (60 + (i * interval)) % 88 + 21
            # pitch = int(((60 + (int(scaled_range[i]) * interval)) % 88)**2.) + 21
            # pitch = int((1.-(((60 + (i * interval)) % 88)/88.))**0.5 * 88) + 21

            vel = int(60 + i * 1.0) % 64 + 60

            length = ((i / note_amt) * 1. + 0.01) % 4.
            length = round(length, 4)

            # ioi = random.choice([1, 2, 7]) * 0.05
            ioi = random.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]) * 0.01
            # ioi = random.randrange(1,4,1)
            # ioi = (math.pow(2., ioi) / 8.) * 0.5
            # ioi = round(math.pow(random.randrange(1,5)/5., 2.) * 2., 5)
            # ioi *= 0.5
            # ioi = 0.1

            midi_data = [pitch, vel, length]

            separator = f'{"=" * 26}'
            nth_note = f'{f"{separator}   {i + 1}th note   {separator}":^72s}'
            # nth_note = f'{nth_note:^70s}'
            print(nth_note)
            self.print_midi_data([*midi_data, ioi])
            self.output_midi(midi_data)
            time.sleep(ioi)

        self.quit()

    def test_arpeggio(self):
        for i in range(88):
            separator = f'{"=" * 26}'
            nth_note = f'{f"{separator}   {i + 1}th note   {separator}":^72s}'
            print(nth_note)
            i /= 87
            self.play([i, i, 0.1, 0.1])
        self.quit()


# m = MidiNote(output_device="loopMIDI Port")
# m.demo()
# m = MidiNote(input_device="Akai MPD26")


class MidiController(threading.Thread):
    def __init__(self, idx=None, chnl=None, ctrl=None, verbose=1, normalize=0):
        """ Define a device, channel and controllers to listen to. Query
        class instance to retrieve a dict of midi_tools data_tools received.

        Example:
        midi_ctrl = MidiController('Akai MPD26')
        midi_ctrl.start()
        chnl, ctrl = 1, (20, 21, 22, 23, 24, 25)
        while not midi_ctrl.quit_flag:
            d = midi_ctrl(chnl, ctrl)
            if d is not None:
                print('{channel{controller{value}}} ---', d)
            time.sleep(0.01)
        print('THE END')
        """
        self.normalize = normalize
        self.verbose = verbose
        input_devices = pm_get_input_devices()
        self.input_devices = dict(zip(*input_devices))
        print("-" * 45)
        print("QUIT SIGNAL is 'controller' = 117 (stop button)\n")
        for k, v in self.input_devices.items():
            print(f'"{k}" at input index {v}')
        print("-" * 45)
        self.idx = idx
        self.chnl = chnl
        self.ctrl = ctrl
        if isinstance(idx, int):
            self.idx = idx
            print(f'Found {idx}, using index {self.idx}...')
        elif isinstance(idx, str):
            self.idx = self.input_devices[idx]
            print(f'Found {idx}, using index {self.idx}...')
        self.s = Server(duplex=0)
        self.data = {}
        self.numeric_data = {}
        self.program_dict = {}
        self.data_out = self.data
        self.query_dict = {}
        self.quit_flag = 0
        self.internal_chnl = None
        threading.Thread.__init__(self)

    def __call__(self, chnl=None, ctrl=None, *args, **kwargs):
        if chnl is None:
            chnl = self.chnl
        if ctrl is None:
            ctrl = self.ctrl
        if isinstance(ctrl, int):
            ctrl = [ctrl]
        with contextlib.suppress(Exception):
            if self.data_out.keys() is not None:
                if a := {k: v for k, v in sorted(self.data_out[chnl].items()) if k in ctrl}:
                    if self.normalize:
                        norm_arr = np.array(list(a.values())) / 127.0
                        a |= dict(zip(a.keys(), norm_arr))
                    self.query_dict[chnl] = a
                if self.query_dict:
                    return self.query_dict

    def run(self):
        self.use_device()

        def ctl_scan(ctlnum, midichnl):
            self.internal_chnl = midichnl

        def event(status, data1, data2):
            self.data["channel"] = self.internal_chnl
            self.data["controller"] = data1
            self.data["status"] = status
            self.data["value"] = data2

            self.program_dict[data1] = data2
            self.numeric_data[self.internal_chnl] = self.program_dict

        ctl = CtlScan2(ctl_scan, toprint=False)
        raww = RawMidi(event).play()

        last_value = list(self.data.values())

        while not self.quit_flag:
            current_value = list(self.data.values())

            if last_value != current_value:
                self.data_out = self.numeric_data
                if self.data['controller'] == 117:
                    self.quit()
            else:
                self.data_out = None
            if self.data_out and self.verbose:
                print(self.__call__())
            time.sleep(0.01)
            last_value = current_value

    def use_device(self):
        self.s.setMidiInputDevice(self.idx)
        self.s.boot().start()
        print("Play with your Midi controller...")

    def quit(self):
        print("QUIT signal received...")
        self.quit_flag = 1
        self.s.stop()
        self.s.shutdown()


# midi_ctrl = MidiController('Akai MPD26', 1, (20,21,22), normalize=1, verbose=0)
# midi_ctrl.start()
# while not midi_ctrl.quit_flag:
#     d = midi_ctrl()
#     if d is not None:
#         print('{channel{controller{value}}} ---', d)
#     time.sleep(0.01)
