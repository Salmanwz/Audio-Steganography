from tkinter import *
import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
import os, math, struct, wave
import base64
import ast
import matplotlib.pyplot as plt
import numpy as np
from math import log10, sqrt
import RootPage as rp
import AdminLogin as al

dict1 = {'init': 'done!'}

class AdmHmPg(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def UsrHid():
            win = Toplevel()
            win.geometry('500x500')

            def hidepro():
                try:
                    smg1, smad1, lad1
                except NameError:
                    cp = Label(win, text="File(s) not selected", fg='red', width=40, font=("bold", 10))
                    cp.place(x=100, y=100)

                else:
                    print(smg1, smad1, lad1)

                    directory = os.path.dirname('hi_process/prsad.wav')
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    soutput_path = 'hi_process/prsad.wav'

                    citer = 'smg2smad'
                    hide_data(smad1, smg1, soutput_path, citer)

            def smg():
                global smg1
                path = tkinter.filedialog.askopenfilename(initialdir="./Inputs/", title="Select file",
                                                          filetypes=(("all files", "*.*"), ("Text File", "*.txt"), ("Pdf file", "*.pdf"), ("Jpg File", "*.jpg"), ("Png File", "*.png")))
                t = os.path.splitext(path)
                type = t[1]
                dict1.update({'type': type})
                print(dict1)

                if (type != '.txt'):
                    directory = os.path.dirname('File process/')
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    with open(path, 'rb') as File:
                        str = base64.b64encode(File.read())
                        f = open("File process/imgtotxt.txt", "wb")
                        f.write(str)
                        f.close()
                    smg1 = "File process/imgtotxt.txt"
                else:
                    smg1 = path

            def smad():
                global smad1
                smad1 = tkinter.filedialog.askopenfilename(initialdir="./Inputs/Audio Files/", title="Select file",
                                                           filetypes=(("WAVE Audio", "*.wav"), ("all files", "*.*")))

            def lad():
                global lad1
                lad1 = tkinter.filedialog.askopenfilename(initialdir="./Inputs/Audio Files/", title="Select file",
                                                          filetypes=(("WAVE Audio", "*.wav"), ("all files", "*.*")))

            def hide_data(sound_path, file_path, output_path, citer):
                if (citer == 'smg2smad'):
                    global sound, params, n_frames, n_samples, fmt, mask, smallest_byte, required_LSBs, filesize

                    def prepare(sound_path):
                        global sound, params, n_frames, n_samples, fmt, mask, smallest_byte, required_LSBs, filesize
                        sound = wave.open(sound_path, "r")
                        print(citer)
                        params = sound.getparams()
                        print("params=", params)
                        num_channels = sound.getnchannels()
                        print("num_channels", num_channels)
                        sample_width = sound.getsampwidth()
                        print("sample_width", sample_width)
                        n_frames = sound.getnframes()
                        print("n_frames", n_frames)
                        n_samples = n_frames * num_channels
                        print("n_samples", n_samples)
                        filesize = os.stat(file_path).st_size
                        filesizesa = os.stat(sound_path).st_size
                        required_LSBs = math.ceil(filesize * 8 / n_samples)
                        print("filesize", filesize)
                        print(" required_LSBs", required_LSBs)
                        dict1.update({'smglsb': required_LSBs, 'smgfs': filesize})
                        print(dict1)

                        if (sample_width == 1):
                            fmt = "{}B".format(n_samples)
                            print("fmt", fmt)

                            mask = (1 << 8) - (1 << required_LSBs)

                            print("mask", mask)

                            smallest_byte = -(1 << 8)
                            print("smallest_byte", smallest_byte)
                        elif (sample_width == 2):
                            fmt = "{}h".format(n_samples)
                            print("fmt", fmt)

                            mask = (1 << 15) - (1 << required_LSBs)
                            print("mask", mask)
                            smallest_byte = -(1 << 15)
                            print("smallest_byte", smallest_byte)
                        else:
                            raise ValueError("File has an unsupported bit-depth")

                        if (filesize >= filesizesa):
                            cp = Label(win, text="The size of small audio should be more", fg='red', width=40, font=("bold", 10))
                            cp.place(x=100, y=100)
                            raise ValueError('please use bigger "small audio file" to reduce noise and have better stego object')

                    prepare(sound_path)

                    max_bytes_to_hide = (n_samples * required_LSBs) // 8

                    if (filesize > max_bytes_to_hide):
                        required_LSBs = math.ceil(filesize * 8 / n_samples)
                        print("required_LSBs", required_LSBs)
                        raise ValueError("Input file too large to hide, "
                                         "requires {} LSBs, using {}"
                                         .format(required_LSBs, required_LSBs))

                    print("Using {} B out of {} B".format(filesize, max_bytes_to_hide))

                    raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
                    sound.close()

                    input_data = memoryview(open(file_path, "rb").read())

                    data_index = 0
                    sound_index = 0

                    values = []
                    buffer = 0
                    buffer_length = 0
                    done = False

                    while (not done):
                        while (buffer_length < required_LSBs and data_index // 8 < len(input_data)):
                            buffer += (input_data[data_index // 8] >> (data_index % 8)
                                       ) << buffer_length
                            bits_added = 8 - (data_index % 8)
                            buffer_length += bits_added
                            data_index += bits_added

                        current_data = buffer % (1 << required_LSBs)
                        buffer >>= required_LSBs
                        buffer_length -= required_LSBs

                        while (sound_index < len(raw_data) and
                               raw_data[sound_index] == smallest_byte):
                            values.append(struct.pack(fmt[-1], raw_data[sound_index]))
                            sound_index += 1

                        if (sound_index < len(raw_data)):
                            current_sample = raw_data[sound_index]
                            sound_index += 1

                            sign = 1
                            if (current_sample < 0):
                                current_sample = -current_sample
                                sign = -1

                            altered_sample = sign * ((current_sample & mask) | current_data)

                            values.append(struct.pack(fmt[-1], altered_sample))

                        if (data_index // 8 >= len(input_data) and buffer_length <= 0):
                            done = True

                    while (sound_index < len(raw_data)):
                        values.append(struct.pack(fmt[-1], raw_data[sound_index]))
                        sound_index += 1

                    sound_steg = wave.open(output_path, "w")
                    sound_steg.setparams(params)
                    sound_steg.writeframes(b"".join(values))
                    sound_steg.close()
                    print("Data hidden over {} audio file".format(output_path))

                    if (os.path.exists(output_path)):
                        citer = 'smad2lad'

                        directory = os.path.dirname('processed/prlad.wav')
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                        s2output_path = 'processed/prlad.wav'
                        hide_data2(lad1, output_path, s2output_path, citer)
                    else:
                        print("File not Found!")

            def hide_data2(sound_path, file_path, output_path, citer):
                if (citer == 'smad2lad'):
                    global sound, params, n_frames, n_samples, fmt, mask, smallest_byte, required_LSBs, filesize

                    def prepare(sound_path):
                        global sound, params, n_frames, n_samples, fmt, mask, smallest_byte, required_LSBs, filesize
                        sound = wave.open(sound_path, "r")
                        print(citer)
                        params = sound.getparams()
                        print("params=", params)
                        num_channels = sound.getnchannels()
                        print("num_channels", num_channels)
                        sample_width = sound.getsampwidth()
                        print("sample_width", sample_width)
                        n_frames = sound.getnframes()
                        print("n_frames", n_frames)
                        n_samples = n_frames * num_channels
                        print("n_samples", n_samples)
                        filesize = os.stat(file_path).st_size
                        required_LSBs = math.ceil(filesize * 8 / n_samples)
                        print("filesize", filesize)
                        print(" required_LSBs", required_LSBs)
                        dict1.update({'sadlsb': required_LSBs, 'sadfs': filesize})
                        print(dict1)

                        if (sample_width == 1):
                            fmt = "{}B".format(n_samples)
                            mask = (1 << 8) - (1 << required_LSBs)

                            smallest_byte = -(1 << 8)
                        elif (sample_width == 2):
                            fmt = "{}h".format(n_samples)
                            mask = (1 << 15) - (1 << required_LSBs)
                            smallest_byte = -(1 << 15)
                        else:
                            # Python's wave module doesn't support higher sample widths
                            raise ValueError("File has an unsupported bit-depth")

                        if (required_LSBs > 9):
                            cp = Label(win, text="The size of large audio should be more", fg='red', width=40, font=("bold", 10))
                            cp.place(x=100, y=100)
                            raise ValueError('please use bigger "large audio" file to reduce noise and have better stego object')

                    prepare(sound_path)

                    max_bytes_to_hide = (n_samples * required_LSBs) // 8

                    if (filesize > max_bytes_to_hide):
                        required_LSBs = math.ceil(filesize * 8 / n_samples)
                        raise ValueError("Input file too large to hide, "
                                         "requires {} LSBs, using {}"
                                         .format(required_LSBs, required_LSBs))

                    print("Using {} B out of {} B".format(filesize, max_bytes_to_hide))

                    raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
                    sound.close()

                    input_data = memoryview(open(file_path, "rb").read())

                    data_index = 0
                    sound_index = 0

                    values = []
                    buffer = 0
                    buffer_length = 0
                    done = False

                    while (not done):
                        while (buffer_length < required_LSBs and data_index // 8 < len(input_data)):
                            buffer += (input_data[data_index // 8] >> (data_index % 8)
                                       ) << buffer_length

                            bits_added = 8 - (data_index % 8)

                            buffer_length += bits_added

                            data_index += bits_added

                        current_data = buffer % (1 << required_LSBs)

                        buffer >>= required_LSBs

                        buffer_length -= required_LSBs

                        while (sound_index < len(raw_data) and
                               raw_data[sound_index] == smallest_byte):
                            values.append(struct.pack(fmt[-1], raw_data[sound_index]))
                            sound_index += 1

                        if (sound_index < len(raw_data)):
                            current_sample = raw_data[sound_index]
                            sound_index += 1

                            sign = 1
                            if (current_sample < 0):
                                current_sample = -current_sample
                                sign = -1

                            altered_sample = sign * ((current_sample & mask) | current_data)

                            values.append(struct.pack(fmt[-1], altered_sample))

                        if (data_index // 8 >= len(input_data) and buffer_length <= 0):
                            done = True

                    while (sound_index < len(raw_data)):
                        values.append(struct.pack(fmt[-1], raw_data[sound_index]))
                        sound_index += 1

                    cp = Label(win, text="Successfully Hidden!", fg='green', width=40, font=("bold", 10))
                    cp.place(x=100, y=100)
                    sound_steg = wave.open(output_path, "w")
                    sound_steg.setparams(params)
                    sound_steg.writeframes(b"".join(values))
                    sound_steg.close()

                    if os.path.exists("File process/imgtotxt.txt"):
                        os.remove("File process/imgtotxt.txt")
                        os.removedirs("File process")
                    print("Data hidden over {} audio file".format(output_path))

                    enc = base64.b64encode(bytes(repr(dict1), "utf-8"))
                    file = open('recover.key', 'wb')
                    file.write(enc)

                    winhi = Toplevel()
                    winhi.geometry('500x500')
                    winhi.title('Hide Success!')

                    label_0 = Label(winhi, text="Hidden Successfully!", width=20, font=("bold", 20))
                    label_0.place(x=90, y=53)
                    label_0 = Label(winhi, text="Files are in following locations", width=25, font=("bold", 15))
                    label_0.place(x=90, y=83)

                    label_1 = Label(winhi, text="Large Audio", width=20, font=("bold", 10))
                    label_1.place(x=80, y=130)
                    entry_1 = Entry(winhi)
                    entry_1.insert(0, "processed/prlad.wav")
                    entry_1.place(x=240, y=130)

                    label_2 = Label(winhi, text="Key", width=20, font=("bold", 10))
                    label_2.place(x=80, y=230)

                    entry_2 = Entry(winhi)
                    entry_2.insert(0, "recover.key")
                    entry_2.place(x=240, y=230)

                    Button(winhi, text='Done!', width=20, bg='green', fg='white', command=winhi.destroy).place(x=180,
                                                                                                               y=280)

            label_0 = Label(win, text="Hide", width=20, font=("bold", 20))
            label_0.place(x=90, y=53)
            ttk.Separator(win).place(x=0, y=90, relwidth=1)

            label_1 = Label(win, text="Secret Msg", width=20, font=("bold", 10))
            label_1.place(x=80, y=130)

            # tk.Radiobutton(win, text='Txt',command=smg,value=1).place(x=260, y=125)
            # tk.Radiobutton(win, text='Image',command=smgi,value=2).place(x=260, y=145)
            # tk.Radiobutton(win, text='PDF', command=smgpdf, value=3).place(x=260, y=165)

            Button(win, text='SELECT', width=15, bg='brown', fg='white', command=smg).place(x=260, y=130)

            label_1 = Label(win, text="Small Audio", width=20, font=("bold", 10))
            label_1.place(x=80, y=180)

            Button(win, text='SELECT', width=15, bg='brown', fg='white', command=smad).place(x=260, y=180)

            label_2 = Label(win, text="Large Audio", width=20, font=("bold", 10))
            label_2.place(x=80, y=230)

            Button(win, text='SELECT', width=15, bg='brown', fg='white', command=lad).place(x=260, y=230)

            Button(win, text='Proceed', width=20, bg='green', fg='white', command=hidepro).place(x=180, y=340)
            Button(win, text='Cancel', width=20, bg='red', fg='white', command=win.destroy).place(x=180, y=370)

        def UsrRec():

            win = Toplevel()
            win.geometry('500x500')
            win.title("Recover")

            def RecPro():
                try:
                    rlad1, rlad2
                except NameError:
                    cp = Label(win, text="File(s) not selected", fg='red', width=40, font=("bold", 10))
                    cp.place(x=100, y=100)

                else:
                    file = open(rlad2, 'r')
                    dec = file.read()
                    deco = base64.b64decode(dec).decode("utf-8", "ignore")
                    global dict1
                    dict1 = ast.literal_eval(deco)
                    global smglsb, smgfs, sadlsb, sadfs, type
                    smglsb = dict1['smglsb']
                    smgfs = dict1['smgfs']
                    sadlsb = dict1['sadlsb']
                    sadfs = dict1['sadfs']
                    type = dict1['type']

                    directory = os.path.dirname('re_process/smad.wav')
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    outp = 're_process/smad.wav'
                    recover_data(rlad1, outp, sadlsb, sadfs)

            def rlad():
                global rlad1
                rlad1 = tkinter.filedialog.askopenfilename(initialdir="./processed", title="Select file",
                                                           filetypes=(("WAVE Audio", "*.wav"), ("all files", "*.*")))

            def rkey():
                global rlad2
                rlad2 = tkinter.filedialog.askopenfilename(initialdir="./", title="Select file",
                                                           filetypes=(("Key File", "*.key"), ("all files", "*.*")))

            def recover_data(sound_path, output_path, num_lsb, bytes_to_recover):
                global sound, n_frames, n_samples, fmt, smallest_byte

                def prepare(sound_path):
                    global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
                    sound = wave.open(sound_path, "r")

                    params = sound.getparams()
                    num_channels = sound.getnchannels()
                    sample_width = sound.getsampwidth()
                    n_frames = sound.getnframes()
                    n_samples = n_frames * num_channels

                    if (sample_width == 1):
                        fmt = "{}B".format(n_samples)

                        mask = (1 << 8) - (1 << num_lsb)
                        smallest_byte = -(1 << 8)
                    elif (sample_width == 2):
                        fmt = "{}h".format(n_samples)
                        mask = (1 << 15) - (1 << num_lsb)

                        smallest_byte = -(1 << 15)
                    else:
                        raise ValueError("File has an unsupported bit-depth")

                prepare(sound_path)

                raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
                mask = (1 << num_lsb) - 1
                output_file = open(output_path, "wb+")

                data = bytearray()
                sound_index = 0
                buffer = 0
                buffer_length = 0
                sound.close()

                while (bytes_to_recover > 0):

                    next_sample = raw_data[sound_index]
                    if (next_sample != smallest_byte):
                        buffer += (abs(next_sample) & mask) << buffer_length
                        buffer_length += num_lsb
                    sound_index += 1

                    while (buffer_length >= 8 and bytes_to_recover > 0):
                        current_data = buffer % (1 << 8)
                        buffer >>= 8
                        buffer_length -= 8
                        data += struct.pack('1B', current_data)
                        bytes_to_recover -= 1

                output_file.write(bytes(data))
                output_file.close()
                print("Data recovered to {} Wave file".format(output_path))

                directory = os.path.dirname('processed/recovered.txt')
                if not os.path.exists(directory):
                    os.makedirs(directory)

                op = 'processed/recovered.txt'
                recover_data2(output_path, op, smglsb, smgfs)

            def recover_data2(sound_path, output_path, num_lsb, bytes_to_recover):
                global sound, n_frames, n_samples, fmt, smallest_byte

                def prepare(sound_path):
                    global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
                    sound = wave.open(sound_path, "r")

                    params = sound.getparams()
                    num_channels = sound.getnchannels()
                    sample_width = sound.getsampwidth()
                    n_frames = sound.getnframes()
                    n_samples = n_frames * num_channels

                    if (sample_width == 1):
                        fmt = "{}B".format(n_samples)
                        mask = (1 << 8) - (1 << num_lsb)

                        smallest_byte = -(1 << 8)
                    elif (sample_width == 2):
                        fmt = "{}h".format(n_samples)
                        mask = (1 << 15) - (1 << num_lsb)
                        smallest_byte = -(1 << 15)
                    else:
                        raise ValueError("File has an unsupported bit-depth")

                prepare(sound_path)

                raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
                mask = (1 << num_lsb) - 1
                output_file = open(output_path, "wb+")

                data = bytearray()
                sound_index = 0
                buffer = 0
                buffer_length = 0
                sound.close()

                while (bytes_to_recover > 0):

                    next_sample = raw_data[sound_index]
                    if (next_sample != smallest_byte):
                        buffer += (abs(next_sample) & mask) << buffer_length
                        buffer_length += num_lsb
                    sound_index += 1

                    while (buffer_length >= 8 and bytes_to_recover > 0):
                        current_data = buffer % (1 << 8)
                        buffer >>= 8
                        buffer_length -= 8
                        data += struct.pack('1B', current_data)
                        bytes_to_recover -= 1

                output_file.write(bytes(data))
                output_file.close()

                if os.path.exists("processed/recovered.jpg"):
                    os.remove("processed/recovered.jpg")
                print("Data recovered to {} text file".format(output_path))

                if (type != '.txt'):
                    file = open(output_path, 'rb')
                    byte = file.read()
                    file.close()
                    decodeit = open('processed/recovered{}'.format(type), 'wb')
                    decodeit.write(base64.b64decode((byte)))
                    decodeit.close()

                    if os.path.exists("processed/recovered.txt"):
                        os.remove("processed/recovered.txt")

                var1 = StringVar()
                def name(type):
                    switcher = {
                        '.pdf': 'PDF',
                        '.jpg': 'Image',
                        '.jpeg': 'Image',
                        '.png': 'Image' ,
                        '.txt': 'Text'
                    }
                    return switcher.get(type)
                var1.set('{} file'.format(name(type)))

                def dlg():
                    cp = Label(win, text="Successfully Recovered!", fg='green', width=40, font=("bold", 10))
                    cp.place(x=100, y=100)

                    winhi = Toplevel()
                    winhi.geometry('500x500')
                    winhi.title('Recover Success!')

                    label_0 = Label(winhi, text="Recovered Successfully!", width=20, font=("bold", 20))
                    label_0.place(x=90, y=53)
                    label_0 = Label(winhi, text="Files are in following locations", width=25, font=("bold", 15))
                    label_0.place(x=90, y=83)

                    label_1 = Label(winhi, text="Small Audio", width=20, font=("bold", 10))
                    label_1.place(x=80, y=130)
                    entry_1 = Entry(winhi)
                    entry_1.insert(0, "re_process/")
                    entry_1.place(x=240, y=130)

                    label_2 = Label(winhi, textvariable=var1, width=20, font=("bold", 10))
                    label_2.place(x=80, y=230)

                    entry_2 = Entry(winhi)
                    entry_2.insert(0, "processed/")
                    entry_2.place(x=240, y=230)

                    Button(winhi, text='Done!', width=20, bg='green', fg='white', command=winhi.destroy).place(x=180,
                                                                                                               y=280)

                dlg()

            label_0 = Label(win, text="Recover", width=20, font=("bold", 20))
            label_0.place(x=90, y=53)
            ttk.Separator(win).place(x=0, y=90, relwidth=1)

            label_1 = Label(win, text="Audio File", width=20, font=("bold", 10))
            label_1.place(x=80, y=130)

            Button(win, text='SELECT', width=15, bg='brown', fg='white', command=rlad).place(x=260, y=130)

            label_1 = Label(win, text="Recovery Key", width=20, font=("bold", 10))
            label_1.place(x=80, y=180)
            Button(win, text='SELECT', width=15, bg='brown', fg='white', command=rkey).place(x=260, y=180)

            Button(win, text='Proceed', width=20, bg='green', fg='white', command=RecPro).place(x=180, y=340)
            Button(win, text='Cancel', width=20, bg='red', fg='white', command=win.destroy).place(x=180, y=370)

        def UsrAna():
            win = Toplevel()
            win.geometry('500x500')
            win.title("Analysis")

            def AnaPro(trig):
                try:
                    rlad1, rlad2
                except NameError:
                    cp = Label(win, text="File(s) not selected", fg='red', width=40, font=("bold", 10))
                    cp.place(x=100, y=100)

                else:
                    if (trig == 'asp'):
                        Spectrogram(rlad1,rlad2)
                    else:
                        PSNR(rlad1,rlad2)

            def oad():
                global rlad1
                rlad1 = tkinter.filedialog.askopenfilename(initialdir="./Inputs/Audio Files", title="Select file",
                                                           filetypes=(("WAVE Audio", "*.wav"), ("all files", "*.*")))

            def sad():
                global rlad2
                rlad2 = tkinter.filedialog.askopenfilename(initialdir="./processed", title="Select file",
                                                           filetypes=(("WAVE Audio", "*.wav"), ("all files", "*.*")))

            def Spectrogram(original, compressed):
                raw = wave.open(original, 'r')
                signal = raw.readframes(-1)
                signal = np.frombuffer(signal, dtype="int16")

                f_rate = raw.getframerate()

                time = np.linspace(
                    0,
                    len(signal) / f_rate,
                    num=len(signal)
                )

                stego = wave.open(compressed, 'r')
                signal1 = stego.readframes(-1)
                signal1 = np.frombuffer(signal1, dtype="int16")

                f_rate1 = stego.getframerate()

                time1 = np.linspace(
                    0,
                    len(signal1) / f_rate1,
                    num=len(signal1)
                )

                fig = plt.figure()
                fig.set_figheight(5)
                fig.set_figwidth(15)

                plt.subplot(1, 2, 1)
                plt.plot(time, signal)
                plt.title("Original")
                plt.xlabel('Time')
                plt.ylabel('Amplitude')

                plt.subplot(1, 2, 2)
                plt.plot(time1, signal1)
                plt.title("Stego")
                plt.xlabel('Time')
                plt.ylabel('Amplitude')

                plt.show()

            def PSNR(original, compressed):
                original = wave.open(original, 'r')
                compressed = wave.open(compressed, 'r')

                originalSignal = original.readframes(-1)
                originalSignal = np.frombuffer(originalSignal, dtype="uint8")

                compressedSignal = compressed.readframes(-1)
                compressedSignal = np.frombuffer(compressedSignal, dtype="uint8")

                mse = np.mean((originalSignal - compressedSignal) ** 2)
                if (mse == 0):
                    var.set("PSNR value is 100 dB")
                    return
                print('mse value {}'.format(mse))
                max_pixel = 255
                psnr = 20 * log10(max_pixel / sqrt(mse))
                var.set("PSNR value is {:.5f} dB".format(psnr))

            var = StringVar()
            label_0 = Label(win, text="Analysis", width=20, font=("bold", 20))
            label_0.place(x=90, y=53)
            ttk.Separator(win).place(x=0, y=90, relwidth=1)

            label_1 = Label(win, text="Original Audio File", width=20, font=("bold", 10))
            label_1.place(x=80, y=130)
            Button(win, text='SELECT', width=15, bg='brown', fg='white', command=oad).place(x=260, y=130)

            label_1 = Label(win, text="Stego Audio File", width=20, font=("bold", 10))
            label_1.place(x=80, y=180)
            Button(win, text='SELECT', width=15, bg='brown', fg='white', command=sad).place(x=260, y=180)

            Button(win, text='Spectrogram', width=20, bg='green', fg='white', command=lambda: AnaPro('asp')).place(x=180, y=240)
            Button(win, text='PSNR', width=20, bg='green', fg='white', command=lambda: AnaPro('psnr')).place(x=180, y=270)
            label_2 = Label(win, textvariable=var, width=25, font=("bold", 14))
            label_2.place(x=110, y=300)

            Button(win, text='Cancel', width=20, bg='red', fg='white', command=win.destroy).place(x=180, y=350)

        var = StringVar()
        name = 'user'
        print(name)
        var.set("Hello, {}!".format(name))
        label_0 = Label(self, textvariable= var, width=20, font=("bold", 20))
        label_0.place(x=100, y=53)

        Button(self, text='Signout', width=8, bg='black', fg='white',
               command=lambda: controller.show_frame(rp.RootPage)).place(x=390, y=53)

        ttk.Separator(self).place(x=0, y=120, relwidth=1)
        label_1 = Label(self, text="Steganography", width=20, font=("default", 14))
        label_1.place(x=100, y=130)

        Button(self, text='Hide', width=24, bg='brown', fg='white', command=UsrHid).place(x=123, y=160)
        Button(self, text='Extract', width=24, bg='brown', fg='white', command=UsrRec).place(x=123, y=190)
        Button(self, text='Analysis', width=24, bg='brown', fg='white', command=UsrAna).place(x=123, y=220)

        ttk.Separator(self).place(x=0, y=270, relwidth=1)