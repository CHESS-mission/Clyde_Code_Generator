# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:56:29 2022

@author: micha
"""

# Clyde_UART and Clyde_Timer are classes storing important data (i.e. registers) of the peripherals
from clyde_uart import Clyde_UART
from clyde_timer import Clyde_Timer


"""
This class generates assembly code for the Clyde SoC. 
It is instantiated for every field in the program generator. 

Be aware that (at the moment) only code controlling the peripherals is implemented.
Other code can be added using the add_assembly_code function
"""
class Clyde_Code_Generator:
    def __init__(self, intendation=0):
        self.apb_slots = {
            'timer': 0,
            'uart': 1
            }
        self.intendation = intendation
        self.code = ""
        

    # --------------------------------
    #           Basic Code
    #---------------------------------

    def add_comment(self, comment):
        self._append_codeline(r"// " + comment)
        
    def add_assembly_code(self, assembly_code): 
        self._append_codeline(assembly_code)
        
    def add_label(self, label): 
        self._append_codeline(f"${label}")
        
            
    # --------------------------------
    #           UART
    #---------------------------------
            
    def init_uart(self):
        self._append_codeline(f"// init uart function to be implemented")

    def print_to_uart(self, string):
        apb_slot = self.apb_slots['uart']
        register = Clyde_UART.registers['TxData']
        for char in string: 
            self._append_codeline(f"APBWRT DAT8 {apb_slot} {register} '{char}'")

    # --------------------------------
    #           Timer
    #---------------------------------
    
    def configure_timer(self, timer_enable=True, interrupt_enable=True, one_shot=False):
        # APBWRT DAT 0 0x08 0x0003
        apb_slot = self.apb_slots['timer']
        register = Clyde_Timer.registers['TimerControl']
        value = 0
        if timer_enable:
            value += 1
        if interrupt_enable:
            value += 2
        if one_shot:
            value +=  4
        self._append_codeline(f"APBWRT DAT {apb_slot} {register} {value}")

    def load_timer_value(self, timer_value):
        apb_slot = self.apb_slots['timer']
        register = Clyde_Timer.registers['TimerLoad']
        self._append_codeline(f"APBWRT DAT {apb_slot} {register} {timer_value}")
        
    def clear_timer_interrupt(self):
        apb_slot = self.apb_slots['timer']
        register = Clyde_Timer.registers['TimerINTClr']
        self._append_codeline(f"APBWRT DAT {apb_slot} {register} 0x0000")
        
    # Internal functions
    
    #add a new line of code to the output
    def _append_codeline(self, line): 
        self.code += "    "*self.intendation + line + "\n"
        
        
        
        
        
        

        
class Clyde_Program_Generator:
    def __init__(self):
        self.interrupt_routine = Clyde_Code_Generator(intendation = 1)
        self.main_program = Clyde_Code_Generator(intendation = 1)
        
    # this functions should be modified to allow generation of more complex programs
    def generate_code(self): 
        print("// Code generated by Clyde_Program_Generator")
        print(r"JUMP $MAIN")
        print("// --------------- \n// Interrupt Routine \n// ---------------" )
        print(self.interrupt_routine.code)
        print("    RETISR")
        print("\n")
        print("// --------------- \n// Main Program \n// ---------------" )
        print("$MAIN")
        print(self.main_program.code)
        
if __name__ == "__main__":
    # this is an example showing the usage of this code
    
    # 1. intitialize the program generator
    program = Clyde_Program_Generator()
    
    # the program generator has two fields: interrupt_routine and main_program.
    # commands for both fields have to be entered sequentially. 
    
    # 2. enter the interrupt code
    program.interrupt_routine.add_comment("print to uart")
    program.interrupt_routine.print_to_uart("Hello")
    program.interrupt_routine.add_comment("clear timer interrupt")
    program.interrupt_routine.clear_timer_interrupt()
    
    # 3. enter teh main code
    program.main_program.add_comment("main")
    program.main_program.add_comment("init uart is not needed (default works)")
    program.main_program.init_uart()     
    program.main_program.load_timer_value(0x00FF)
    program.main_program.configure_timer(timer_enable=True, interrupt_enable=True, one_shot=False)
    
    # 4. generate the code (=print the assembly code to the console)
    program.generate_code()
    
    # 5. copy paste the code from the console into Libero