# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 22:08:17 2022

@author: micha
"""

class Clyde_UART: 
    registers = {
        'TxData': '0x000', # write
        'RxData': '0x004', # read
        'Control1': '0x008', #read/write       
        'Control2': '0x00C', #read/write   
        'Control3': '0x014', #read/write
        'Status': '0x010' #read   
        }