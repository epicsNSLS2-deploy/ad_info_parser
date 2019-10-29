#!/usr/bin/env python3

import pyepics
import argparse
import xlsxwriter
import distro
from sys import platform
import os
import subprocess




class WriteableObject:

    def __init__(self, base_pv):
        self.base_pv = base_pv
        self.pv_fields = []


    def read_fields(self):
        values = {}
        for pv in self.pv_fields:
            out = pyepics.caget(self.base_pv + pv)
            values[pv] = out
        return values


class ADIOC(WriteableObject):

    def __init__(self, base_pv):
        super().__init__(base_pv)
        self.pv_fields.append('Manufacturer', 'SerialNumber', 'ModelNumber'









class Writer:

    def __init__(self, beamline, hostname, output_path):
        self.output_path = output_path
        self.beamline = beamline
        self.hostname = hostname


    def write_object(self, writeable_object):
        

