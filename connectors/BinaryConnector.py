# -*- coding: utf-8 -*-
__author__ = 'kbiernat'

import bson
from ComssServiceDevelopment.connectors.tcp.msg_stream_connector import InputMessageConnector, OutputMessageConnector


class OutputBinaryConnector(OutputMessageConnector):
    def send(self, obj):
        self.check_socket_and_open()
        dumped_object = bson.BSON.encode(obj)
        super(OutputBinaryConnector, self).send(dumped_object)


class InputBinaryConnector(InputMessageConnector):
    def read(self):
        msg = super(InputBinaryConnector, self).read()
        return bson.BSON.decode(msg)