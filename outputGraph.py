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

#próg szumu
background_noise = 0.5
current_note = 0

service_controller = DevServiceController("configuration.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("outputGraph", InputObjectConnector(service_controller)) #deklaracja interfejsu wejściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WYJŚCIEM usługi, do której "zaślepka" jest podłączana

connection = service_controller.get_connection("outputGraph")

fig = plt.figure()
#zakres częstotliwości
x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
half_x_f = x_f[1::2]
ax = fig.add_subplot(111, title=TITLE, xlim=(x_f[0], x_f[-1]), ylim=(0, 2 * np.pi * nFFT**2 / RATE))
ax.set_yscale('symlog', linthreshy=nFFT**0.5)
line, = ax.plot(x_f, np.zeros(nFFT - 1))

def data_gen():
    prev_note = 0
    while True:
        data_input = connection.read() #odczyt danych z interfejsu wejściowego
        db_table = np.asarray(data_input["db_table"])

        yield db_table

def animate(db_table):
    line.set_ydata(db_table)
    return line,

def init():
    # Czyszczenie
    line.set_ydata(np.zeros(nFFT - 1))
    return line,

ani = animation.FuncAnimation(fig, animate, data_gen, init_func=init, interval=1000.0/FPS, blit=True)
plt.show()
