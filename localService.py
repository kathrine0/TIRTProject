# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

import threading
from ComssServiceDevelopment.connectors.tcp.stream_connector import InputStreamConnector, OutputStreamConnector
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector, OutputObjectConnector
from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi

import numpy as np
import struct

SAVE = 0.0
TITLE = ''
FPS = 25.0

nFFT = 512
BUF_SIZE = 4 * nFFT
CHANNELS = 2
RATE = 44100


class LocalService(Service):
    def __init__(self): #"nie"konstruktor, inicjalizator obiektu usługi
        super(LocalService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej

    def declare_outputs(self):
        self.declare_output("localOutput", OutputObjectConnector(self))

    def declare_inputs(self):
        self.declare_input("localInput", InputObjectConnector(self))
        self.declare_input("localInput2", InputObjectConnector(self))

    def run(self):
        N_input = self.get_input("localInput") #obiekt interfejsu wejściowego
        data_input = self.get_input("localInput2") #obiekt interfejsu wejściowego

        audio_output = self.get_output("localOutput") #obiekt interfejsu wyjściowego

        while self.running():
            N = N_input.read()
            data = data_input.read()

            #TODO!!!!!! Send it somehow on init
            MAX_y = 32768.0

            y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
            y_L = y[::2]
            y_R = y[1::2]

            Y_L = np.fft.fft(y_L, nFFT)
            Y_R = np.fft.fft(y_R, nFFT)

            # Sewing FFT of two channels together, DC part uses right channel's
            Y = abs(np.hstack((Y_L[-nFFT/2:-1], Y_R[:nFFT/2])))

            audio_output.send(Y)
            #print (audio_data)

if __name__=="__main__":
    sc = ServiceController(LocalService, "configuration.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi