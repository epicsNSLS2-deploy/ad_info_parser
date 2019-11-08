#!/usr/bin/env python3

import epics
import argparse
import xlsxwriter
import distro
from sys import platform
import os
import subprocess
import socket


alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']



class WriteableObject:

    def __init__(self, base_pv):
        self.base_pv = base_pv
        self.pv_fields = ['HOSTNAME', 'ENGINEER']


    def read_fields(self):
        values = {}
        for pv in self.pv_fields:
            out = pyepics.caget(self.base_pv + pv)
            values[pv] = out
        return values


class ADIOC(WriteableObject):

    def __init__(self, base_pv):
        super().__init__(base_pv)
        self.pv_fields = self.pv_fields + ['Manufacturer', 'SerialNumber', 'ModelNumber', 'SDKVersion', 'DriverVersion', 'ADCoreVersion', 'SizeX', 'SizeY', 'DataType', 'ColorMode']




class Writer:

    def __init__(self, beamline, output_fields, output_path):
        self.output_path = output_path
        self.beamline = beamline
        self.hostname = hostname
        self.output_fields = output_fields
        self.general_fields = {}


    def add_general_field(self, field, value):
        self.output_fields.append(field)
        self.general_fields[field] = value


    def write_object(self, writeable_object_list):
        output_workbook = xlsxwriter.Workbook(self.output_path)
        output_worksheet = output_workbook.add_worksheet('{} - {}'.format(self.beamline, socket.gethostname()))
        counter = 0
        output_key = {}
        for field in self.output_fields:
            output_key[field] = alphabet[counter]
            output_worksheet.write('{}1'.format(alphabet[counter]), field)
        ioc_counter = 2
        for writeable_object in writeable_object_list:
            for field in self.general_fields.keys():
                output_worksheet.write('{}{}'.format(output_key[field], ioc_counter), self.general_fields[field])
            values = writeable_object.read_fields()
            for pv in values.keys():
                output_worksheet.write('{}{}'.format(output_key[pv], ioc_counter), values[pv])
        
            ioc_counter = ioc_counter + 1
        


def get_base_pv_list(ioc_location, prefix):
    base_pv_list = []
    for dir in os.listdir(ioc_location):
        ioc_path = os.path.join(ioc_location, dir)
        print(ioc_path)
        if os.path.isdir(ioc_path) and ioc_path.startswith(prefix):
            print(ioc_path)
            if os.path.exists(os.path.join(ioc_path, 'unqiue.cmd')):
                fp = open(os.path.join(ioc_path, 'unqiue.cmd'), )
            elif os.path.exists(os.path.join(ioc_path, 'st.cmd')):
                fp = open(os.path.join(ioc_path, 'st.cmd'))
            lines = fp.readlines()
            for line in lines:
                print(line)
                if line.startswith('epicsEnvSet("PREFIX') or line.startswith("epicsEnvSet('PREFIX"):
                    print(line)
                    line = line.strip()
                    line = line.split(',')[1]
                    line = line.strip()
                    line = line[1:len(line)-1]
                    base_pv_list.append(line)
    return base_pv_list



def parse_args():
    parser = argparse.ArgumentParser(description='A python utility for writing IOC information into an excel spreadsheet.')
    parser.add_argument('-o', '--outputloc', help='Output Excel Spreadsheet')
    parser.add_argument('-i', '--iocloc', help='Location of iocs')
    parser.add_argument('-p', '--prefix', help='Script searches for iocs starting with this prefix, i.e. cam-')
    arguments = vars(parser.parse_args())


    print(get_base_pv_list(arguments['iocloc'], arguments['prefix']))


parse_args()
