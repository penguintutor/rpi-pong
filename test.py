# Test ADC readings from MCP3008
import time
from mcp3008 import MCP3008

mcp = MCP3008()

while True:
    adc0 = mcp.read_adc(0)
    adc1 = mcp.read_adc(1)

    print ("Readings {} {}".format(adc0, adc1))
    time.sleep(1)