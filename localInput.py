# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

from ComssServiceDevelopment.connectors.tcp.object_connector import OutputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi
from audioData import audioData

import pyaudio
import base64

service_controller = DevServiceController("configuration.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("localInput", OutputObjectConnector(service_controller)) #deklaracja interfejsu wyjściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WEJŚCIEM usługi, do której "zaślepka" jest podłączana

SAVE = 0.0
TITLE = ''

nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def main():
    #init audio
    p = pyaudio.PyAudio()

    #Do normalizowania sygnału.
    MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)

    frames = None
    wf = None

    stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=BUF_SIZE)

    # Czytaj n*nFFT ramek ze streama, n > 0
    while True:
        N = max(stream.get_read_available() / nFFT, 1) * nFFT
        data = {"N": N, "data" : base64.b64encode(stream.read(N)), "MAX_y": MAX_y}
        service_controller.get_connection("localInput").send(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
  main()