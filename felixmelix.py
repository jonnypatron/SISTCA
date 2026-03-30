import machine
# Configura o I2C nos pinos que ligaste
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)

print('A verificar dispositivos I2C...')
devices = i2c.scan()

if len(devices) == 0:
    print("Nenhum dispositivo encontrado! Verifica as ligações.")
else:
    print('Dispositivos encontrados:', len(devices))
    for device in devices:
        print("Endereço I2C: ", hex(device))