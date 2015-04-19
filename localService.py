# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

import threading
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector, OutputObjectConnector
from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi

import numpy as np
import struct
import base64

SAVE = 0.0
TITLE = ''

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

    def run(self):
        inputObj = self.get_input("localInput") #obiekt interfejsu wejściowego
        outputObj = self.get_output("localOutput") #obiekt interfejsu wyjściowego

        while self.running():

            data_input = inputObj.read()

            N = data_input["N"]
            audioData = base64.b64decode(data_input["data"])
            MAX_y = data_input["MAX_y"]

            print(MAX_y)

            y = np.array(struct.unpack("%dh" % (N * CHANNELS), audioData)) / MAX_y
            y_L = y[::2]
            y_R = y[1::2]

            Y_L = np.fft.fft(y_L, nFFT)
            Y_R = np.fft.fft(y_R, nFFT)

            # Łączenie kanałów FFT, DC - prawy kanał
            Y = abs(np.hstack((Y_L[-nFFT/2:-1], Y_R[:nFFT/2])))

            output = list(Y)
            outputObj.send(output)
            #print (Y)

if __name__=="__main__":
    sc = ServiceController(LocalService, "configuration.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi