# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

import threading
from ComssServiceDevelopment.connectors.tcp.stream_connector import InputStreamConnector, OutputStreamConnector
from ComssServiceDevelopment.service import Service, ServiceController #import modułów klasy bazowej Service oraz kontrolera usługi

class AndroidService(Service):
    def __init__(self): #"nie"konstruktor, inicjalizator obiektu usługi
        super(AndroidService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej

    def declare_outputs(self):
        pass

    def declare_inputs(self):
        self.declare_input("androidInput", InputStreamConnector(self))

    def run(self):
        audio_input = self.get_input("androidInput") #obiekt interfejsu wejściowego
        #video_output = self.get_output("videoOutput") #obiekt interfejsu wyjściowego

        while self.running():
            audio_data = audio_input.read()
            print (audio_data)

if __name__=="__main__":
    sc = ServiceController(AndroidService, "android_configuration.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi