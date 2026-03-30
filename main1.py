import machine
import time
import ustruct

# Configuração
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
ADXL345_ADDR = 0x53

# Inicializar o sensor (Colocar em modo de medição)
i2c.writeto_mem(ADXL345_ADDR, 0x2D, b'\x08')

def get_accel():
    # Lê 6 bytes (X, Y, Z - 2 bytes cada)
    data = i2c.readfrom_mem(ADXL345_ADDR, 0x32, 6)
    # Converte bytes para inteiros (little-endian)
    x, y, z = ustruct.unpack('<hhh', data)
    return x, y, z

print("Leitura iniciada. Move o sensor para ver a variação!")
print("X | Y | Z")

while True:
    x, y, z = get_accel()
    # Imprime os valores formatados
    print(f"{x:6} | {y:6} | {z:6}")
    time.sleep(0.1) # Lê 10 vezes por segundo