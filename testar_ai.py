import machine
import time
import ustruct
# Nota: A biblioteca ulab ajuda em cálculos matemáticos no Pico
try:
    import ulab.numpy as np
except ImportError:
    import numpy as np # Depende do teu firmware

# 1. Configurar I2C e Sensor (Mesmos pinos de antes)
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADDR = 0x53
i2c.writeto_mem(ADDR, 0x2D, b'\x08')

# 2. Valores de normalização (Usa os valores que o Colab calculou)
# Nota: No relatório, refere que a normalização no "Edge" deve ser igual ao treino.
MIN_VAL = -500 # Ajusta conforme o teu dataset
MAX_VAL = 500

def get_accel():
    data = i2c.readfrom_mem(ADDR, 0x32, 6)
    x, y, z = ustruct.unpack('<hhh', data)
    # Normalização em tempo real
    x_n = (x - MIN_VAL) / (MAX_VAL - MIN_VAL)
    y_n = (y - MIN_VAL) / (MAX_VAL - MIN_VAL)
    z_n = (z - MIN_VAL) / (MAX_VAL - MIN_VAL)
    return [x_n, y_n, z_n]

print("IA Ativa! Move o sensor...")

labels = ["Circulo", "Quadrado", "Triangulo"]

while True:
    entrada = get_accel()
    
    # Aqui o modelo entraria em ação. 
    # Como vais validar rapidamente, vamos focar em ver os dados a chegar
    # prontos para a função model.predict()
    
    print(f"Entrada IA: {entrada}")
    
    # Quando tiveres o firmware com tflite:
    # output = model.predict(entrada)
    # print(f"Gesto detetado: {labels[np.argmax(output)]}")
    
    time.sleep(0.2)