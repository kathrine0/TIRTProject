# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

TITLE = 'Analiza spektrum'
FPS = 25.0

nFFT = 512
RATE = 44100

service_controller = DevServiceController("configuration.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("localOutput", InputObjectConnector(service_controller)) #deklaracja interfejsu wejściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WYJŚCIEM usługi, do której "zaślepka" jest podłączana

connection = service_controller.get_connection("localOutput")

fig = plt.figure()
#zakres częstotliwości
x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
ax = fig.add_subplot(111, title=TITLE, xlim=(x_f[0], x_f[-1]), ylim=(0, 2 * np.pi * nFFT**2 / RATE))
ax.set_yscale('symlog', linthreshy=nFFT**0.5)
line, = ax.plot(x_f, np.zeros(nFFT - 1))

def data_gen():
    while True:
        data_input = connection.read() #odczyt danych z interfejsu wejściowego
        freqs = np.asarray(data_input["freqs"])

        yield freqs
        #yield np.random.rand(10)


def animate(freqs):
    line.set_ydata(freqs)
    return line,

def init():
    # Czyszczenie
    line.set_ydata(np.zeros(nFFT - 1))
    return line,

ani = animation.FuncAnimation(fig, animate, data_gen, init_func=init, interval=1000.0/FPS, blit=True)
plt.show()
