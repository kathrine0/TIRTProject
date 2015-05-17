# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

#import modułów klasy bazowej Service oraz kontrolera usługi
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector, OutputObjectConnector
from ComssServiceDevelopment.service import Service, ServiceController

#https://code.google.com/p/midiutil/
from midiutil.MidiFile import MIDIFile

import numpy as np
import struct
import base64
import analyse

nFFT = 512
BUF_SIZE = 4 * nFFT
CHANNELS = 2
RATE = 44100

class LocalService(Service):
    def __init__(self): #"nie"konstruktor, inicjalizator obiektu usługi
        super(LocalService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej

    def declare_outputs(self):
        self.declare_output("outputGraph", OutputObjectConnector(self))
        self.declare_output("outputPitch", OutputObjectConnector(self))

    def declare_inputs(self):
        self.declare_input("input", InputObjectConnector(self))

    def run(self):
        inputObj = self.get_input("input") #obiekt interfejsu wejściowego
        outputGraph = self.get_output("outputGraph") #obiekt interfejsu wyjściowego
        outputPitch = self.get_output("outputPitch") #obiekt interfejsu wyjściowego
        prev_note = 0

        #init midi
        track = 0
        time = 0
        MyMIDI = MIDIFile(1)
        MyMIDI.addTrackName(track,time,"Sample Track")
        MyMIDI.addTempo(track,time,120)

        try:
            while self.running():
                data_input = inputObj.read()

                N = data_input["N"]
                audioData = base64.b64decode(data_input["data"])
                MAX_y = data_input["MAX_y"]

                y = np.array(struct.unpack("%dh" % (N * CHANNELS), audioData)) / MAX_y
                y_L = y[::2]
                y_R = y[1::2]

                Y_L = np.fft.fft(y_L, nFFT)
                Y_R = np.fft.fft(y_R, nFFT)

                # Łączenie kanałów FFT, DC - prawy kanał
                Y = abs(np.hstack((Y_L[-nFFT/2:-1], Y_R[:nFFT/2])))

                samples = np.fromstring(audioData, dtype=np.int16)

                #wyliczenie dzwieku
                rawnote = analyse.musical_detect_pitch(samples)

                if rawnote is not None:
                    note = np.rint(rawnote)

                    if note != prev_note:
                        #wyślij nutę na wyjście
                        outputPitch.send(note)

                        #MyMIDI.addNote(track,channel,pitch,time,duration,volume)
                        MyMIDI.addNote(0,0,note,time,1,100)
                        time+=1
                        prev_note = note

                output = {"db_table": list(Y)}
                outputGraph.send(output)

        #save midi on exit
        except:
            binfile = open("output.mid", 'wb')
            MyMIDI.writeFile(binfile)
            binfile.close()


if __name__=="__main__":
    sc = ServiceController(LocalService, "configuration.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi