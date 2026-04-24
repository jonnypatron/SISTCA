import machine
import time
import ustruct

# Configuração do Sensor
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADDR = 0x53

try:
    i2c.writeto_mem(ADDR, 0x2D, b'\x08')
except OSError:
    pass

ATRASO = 0.05 

while True:
    try:
        data = i2c.readfrom_mem(ADDR, 0x32, 6)
        x, y, z = ustruct.unpack('<hhh', data)
        # Envia apenas NÚMEROS BRUTOS separados por "|"
        print(f"{x} | {y} | {z}")
    except OSError:
        pass
        
    time.sleep(ATRASO)