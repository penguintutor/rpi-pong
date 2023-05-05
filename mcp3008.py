""" SPI MCP3008 ADC for Raspberry Pi """

import spidev


# SPI is ((0,0)) (SPI 0) or ((0,1)) etc
# Defaults to spi 0, default pins
# On the raspberry pi this is SDI=9 (MISO), SDO=10 (MOSI), SCK=11, CS0=8 (CE0)
class MCP3008():
    def __init__(self, spi=(0,0)):
        self.spi = spidev.SpiDev()
        self.spi.open(*spi)
        self.spi.max_speed_hz=1000000
        
        
    # Returns a value between 0 and 1023
    # On error returns None
    def read_adc(self, channel):
        if (channel < 0 or channel > 7):
            print ("Invalid channel")
            return None
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
    