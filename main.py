import machine
import time
import ustruct
import ai_puro # O ficheiro que criaste acima

# Configuração do Sensor
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADDR = 0x53
i2c.writeto_mem(ADDR, 0x2D, b'\x08')

LABELS = ["Circulo", "Quadrado", "Triangulo"]

def normalizar(v):
    return (v - (-500)) / (500 - (-500))

while True:
    # Ler sensor
    data = i2c.readfrom_mem(ADDR, 0x32, 6)
    x, y, z = ustruct.unpack('<hhh', data)
    
    # Preparar entrada
    inputs = [normalizar(x), normalizar(y), normalizar(z)]
    
    probabilidades = ai_puro.predict(inputs)
    classe_id = probabilidades.index(max(probabilidades))
    
    print(f"Gesto: {LABELS[classe_id]} ({max(probabilidades)*100:.1f}%)")
    
    time.sleep(0.5)