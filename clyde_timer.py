# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 23:33:15 2022

@author: micha
"""

class Clyde_Timer: 
    registers = {
        'TimerLoad': '0x00', # read/write
        'TimerValue': '0x04', # read
        'TimerControl': '0x08', #read/write       
        'TimerPrescale': '0x0C', #read/write   
        'TimerINTClr': '0x10', #write
        'TimerRIS': '0x014', #read  
        'TimerMIS': '0x18' #read
        }