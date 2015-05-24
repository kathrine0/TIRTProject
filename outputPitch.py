# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

import Tkinter as tk

from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

service_controller = DevServiceController("configuration.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("pitchOutput", InputObjectConnector(service_controller)) #deklaracja interfejsu wejściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WYJŚCIEM usługi, do której "zaślepka" jest podłączana

# while True:
#     note = connection.read() #odczyt danych z interfejsu wejściowego
#     print(note)
#     label.configure(text=note)

class App():

    def __init__(self):
        self.connection = service_controller.get_connection("pitchOutput")

        self.root = tk.Tk()
        self.root.geometry("200x200")
        self.label = tk.Label(text="", font=("Helvetica", 40), width=150)
        self.label.pack()
        self.update_note()
        self.root.mainloop()

    def update_note(self):
        note = self.connection.read() #odczyt danych z interfejsu wejściowego
        self.label.configure(text=self.midi_to_note(note))
        self.root.after(100, self.update_note)

    def midi_to_note(self, note):

        noteMap = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B",
           12: "C", 13: "C#", 14: "D", 15: "D#", 16: "E", 17: "F", 18: "F#", 19: "G", 20: "G#", 21: "A", 22: "A#", 23: "B",
           24: "C", 25: "C#", 26: "D", 27: "D#", 28: "E", 29: "F", 30: "F#", 31: "G", 32: "G#", 33: "A", 34: "A#", 35: "B",
           36: "C", 37: "C#", 38: "D", 39: "D#", 40: "E", 41: "F", 42: "F#", 43: "G", 44: "G#", 45: "A", 46: "A#", 47: "B",
           48: "C", 49: "C#", 50: "D", 51: "D#", 52: "E", 53: "F", 54: "F#", 55: "G", 56: "G#", 57: "A", 58: "A#", 59: "B",
           60: "C", 61: "C#", 62: "D", 63: "D#", 64: "E", 65: "F", 66: "F#", 67: "G", 68: "G#", 69: "A", 70: "A#", 71: "B",
           72: "C", 73: "C#", 74: "D", 75: "D#", 76: "E", 77: "F", 78: "F#", 79: "G", 80: "G#", 81: "A", 82: "A#", 83: "B",
           84: "C", 85: "C#", 86: "D", 87: "D#", 88: "E", 89: "F", 90: "F#",91: "G", 92: "G#",93: "A", 94: "A#", 95: "B",
           96: "C",97: "C#", 98: "D", 99: "D#", 100: "E", 101: "F", 102: "F#", 103: "G", 104: "G#", 105: "A", 106: "A#", 107: "B",
           108: "C", 109: "C#", 110: "D", 111: "D#", 112: "E", 113: "F", 114: "F#", 115: "G", 116: "G#", 117: "A", 118: "A#", 119: "B",
           120: "C", 121: "C#", 122: "D", 123: "D#", 124: "E", 125: "F", 126: "F#", 127: "G"}

        if 0 <= note <= 127:
            return noteMap[note]
        else:
            return "?"

app=App()