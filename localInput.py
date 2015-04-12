# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

from ComssServiceDevelopment.connectors.tcp.stream_connector import OutputStreamConnector #import modułów konektora msg_stream_connector
from ComssServiceDevelopment.connectors.tcp.object_connector import OutputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

import pyaudio
import struct
import wave
import numpy as np

service_controller = DevServiceController("configuration.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("localInput", OutputObjectConnector(service_controller)) #deklaracja interfejsu wyjściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WEJŚCIEM usługi, do której "zaślepka" jest podłączana
service_controller.declare_connection("localInput2", OutputObjectConnector(service_controller)) #deklaracja interfejsu wyjściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WEJŚCIEM usługi, do której "zaślepka" jest podłączana

SAVE = 0.0
TITLE = ''
FPS = 25.0

nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def main():
    #init audio
    p = pyaudio.PyAudio()

    # Used for normalizing signal. If use paFloat32, then it's already -1..1.
    #Because of saving wave, paInt16 will be easier.
    MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)

    frames = None
    wf = None

    stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=BUF_SIZE)

    # Read n*nFFT frames from stream, n > 0
    N = max(stream.get_read_available() / nFFT, 1) * nFFT
    data = stream.read(N)

    service_controller.get_connection("localInput").send(N)
    service_controller.get_connection("localInput2").send(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
  main()