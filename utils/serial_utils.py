#!/usr/bin/env python3


def write_to_screen(ser, string: str, line_no: int):
    '''
    Write a string to the 16x2 display of the arduino screen.
    ARGS:
        ser: serial object representing the arduino.
        string: string that you would like to write.
        line_no: [0,1] line that you would like to write to.
    '''
    assert line_no in [0,1]
    string = replace_degree_symbol(string)
    string = f"{line_no}:{string}\n".encode('latin-1')
    ser.write(string)


def replace_degree_symbol(string):
    '''
    Replaces the degrees symbol (°) with the bytecode readable by serial.
    '''
    string = string.replace("°", "\xDF")
    return string
