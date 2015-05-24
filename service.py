# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

#import modułów klasy bazowej Service oraz kontrolera usługi
from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector, OutputObjectConnector
from ComssServiceDevelopment.service import Service, ServiceController

import threading

class LocalService(Service):
    def __init__(self): #"nie"konstruktor, inicjalizator obiektu usługi
        super(LocalService, self).__init__() #wywołanie metody inicjalizatora klasy nadrzędnej

    def declare_outputs(self):
        self.declare_output("graphOutput", OutputObjectConnector(self))
        self.declare_output("pitchOutput", OutputObjectConnector(self))

    def declare_inputs(self):
        self.declare_input("graphInput", InputObjectConnector(self))
        self.declare_input("pitchInput", InputObjectConnector(self))

    def run(self):
        threading.Thread(target=self.watch_graph).start()
        threading.Thread(target=self.watch_pitch).start()

    def watch_graph(self):
        graphInput = self.get_input("graphInput") #obiekt interfejsu wejściowego
        outputGraph = self.get_output("graphOutput") #obiekt interfejsu wyjściowego
        while True:
            graph = graphInput.read()
            outputGraph.send(graph)

    def watch_pitch(self):
        pitchInput = self.get_input("pitchInput") #obiekt interfejsu wejściowego
        outputPitch = self.get_output("pitchOutput") #obiekt interfejsu wyjściowego
        while True:
            pitch = pitchInput.read()
            outputPitch.send(pitch)

if __name__=="__main__":
    sc = ServiceController(LocalService, "configuration.json") #utworzenie obiektu kontrolera usługi
    sc.start() #uruchomienie usługi