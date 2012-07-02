# -*- coding: utf-8 -*-

import io
import time
import serial

class Dmr5200(object):
    """
    Representation of a connection to a DMR-5200 digital multimeter.
    """
    def __init__(self, port, timeout=2):
        """
        Opens the serial connection to the meter.
            port    - The platform dependent serial port string
            timeout - The timeout (in seconds) to use for serial read/write operations 
        """
        self.ser = serial.Serial(port, baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=timeout)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser), newline='\r')
    
    def request(self):
        """
        Request one reading from the meter.  None will be returned if any error
        occured when processing the returned data, otherwise a dictionary with
        the following fields will be returned:
        
        {
            'function': <meter function string>,
            'value': <reading value>,
            'units': <measurement units string>,
            'timestamp': <timestamp of reading reception>,
            'raw': <raw serial message string>
        }
        
        'function' may be one of "DC", "AC", "RES", "FR", "CAP", "IND", "TEMP",
            "LOG", "BUZ", or "DIO"
        'value' may be numeric, True/False/None for logic levels, True/False
            for continuity, or one of "OPEN"/"SHORT"/"GOOD" for the diode
            setting, or None if it should be numeric but the meter registered
            an overload condition
        'units' is a string describing the measurement units, or None if not
            applicable
        'timestamp' is an arbitary floating point time value in seconds which
            can be used to determine the actual interval between completed
            readings
        'raw' is the actual string read from the serial port, including the
            trailing carriage return character
        """
        self.ser.write('\r')
        line = self.sio.readline()
        if len(line) < 6:
            return None
        parts = line.split()
        
        result = {
            'function': parts[0],
            'value': None,
            'units': None,
            'timestamp': time.time(),
            'raw': line
        }
        if parts[0] in ["DC", "AC", "RES", "FR", "CAP", "IND", "TEMP"]:
            try:
                result['value'] = float(parts[1])
                result['units'] = parts[2]
                if parts[0] == "TEMP":
                    result['units'] = u"°C"
                elif parts[0] == "RES":
                    if parts[2] == "MOHM":
                        result['units'] = u"MΩ"
                    elif parts[2] == "OHM":
                        result['units'] = u"Ω"
            except ValueError:
                result['value'] = None
            except IndexError:
                return None
        elif parts[0] == "LOG":
            try:
                result['value'] = {'LOW': False, 'HIGH': True, 'UNDET': None}[parts[1]]
            except IndexError:
                return None
        elif parts[0] == "BUZ":
            try:
                result['value'] = {'OPEN': False, 'SHORT': True}[parts[1]]
            except IndexError:
                return None
        elif parts[0] == "DIO":
            try:
                if parts[1] in ["OPEN", "SHORT", "GOOD"]:
                    result['value'] = parts[1]
                else:
                    return None
            except IndexError:
                return None
        return result
    
