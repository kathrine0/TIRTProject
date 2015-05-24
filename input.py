# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

from ComssServiceDevelopment.connectors.tcp.object_connector import OutputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

import pyaudio
import numpy as np
import struct
import analyse
#https://code.google.com/p/midiutil/
from midiutil.MidiFile import MIDIFile

service_controller = DevServiceController("configuration.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("graphInput", OutputObjectConnector(service_controller)) #deklaracja interfejsu wyjściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WEJŚCIEM usługi, do której "zaślepka" jest podłączana
service_controller.declare_connection("pitchInput", OutputObjectConnector(service_controller)) #deklaracja interfejsu wyjściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WEJŚCIEM usługi, do której "zaślepka" jest podłączana

nFFT = 4086
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def main():
    #init midi
    track = 0
    time = 0
    MyMIDI = MIDIFile(1)
    MyMIDI.addTrackName(track,time,"Sample Track")
    MyMIDI.addTempo(track,time,120)

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

    note = 0;
    prev_note = -1;

    try:
        while True:
            N = max(stream.get_read_available() / nFFT, 1) * nFFT
            audioData = stream.read(N);
            # data = {"N": N, "data" : base64.b64encode(stream.read(N)), "MAX_y": MAX_y}
            # service_controller.get_connection("input").send(data)

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

                    #MyMIDI.addNote(track,channel,pitch,time,duration,volume)
                    #MyMIDI.addNote(0,0,note,time,1,100)
                    time+=1
                    prev_note = note

            #wyślij nutę na wyjście
            service_controller.get_connection("pitchInput").send(note)

            if list(Y) is not None:
                service_controller.get_connection("graphInput").send(list(Y))

    #save midi on exit
    except:
        raise
        binfile = open("output.mid", 'wb')
        MyMIDI.writeFile(binfile)
        binfile.close()
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == '__main__':
  main()