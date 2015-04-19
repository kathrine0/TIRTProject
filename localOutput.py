# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

import numpy as np

from ComssServiceDevelopment.connectors.tcp.object_connector import InputObjectConnector
from ComssServiceDevelopment.development import DevServiceController #import modułu klasy testowego kontrolera usługi

service_controller = DevServiceController("configuration.json") #utworzenie obiektu kontroletra testowego, jako parametr podany jest plik konfiguracji usługi, do której "zaślepka" jest dołączana
service_controller.declare_connection("localOutput", InputObjectConnector(service_controller)) #deklaracja interfejsu wejściowego konektora msg_stream_connector, należy zwrócić uwagę, iż identyfikator musi być zgodny z WYJŚCIEM usługi, do której "zaślepka" jest podłączana

connection = service_controller.get_connection("localOutput")

while True: #główna pętla programu
    data_input = connection.read() #odczyt danych z interfejsu wejściowego
    freqs = (data_input)


    print(freqs)
