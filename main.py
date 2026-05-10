import machine
import time
import ustruct
import gc

gc.collect()
import ai_puro

time.sleep(2)

i2c_sensor = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADDR_SENSOR = 0x53
try:
    i2c_sensor.writeto_mem(ADDR_SENSOR, 0x2D, b'\x08')
except OSError:
    pass

lcd_ligado = False
try:
    from machine_i2c_lcd import I2cLcd
    i2c_lcd = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=400000)
    try:
        lcd = I2cLcd(i2c_lcd, 0x27, 4, 20)
    except:
        lcd = I2cLcd(i2c_lcd, 0x3f, 4, 20)
    lcd_ligado = True
except:
    pass

LABELS = ["Circulo", "Quadrado", "Repouso", "Triangulo"]
PONTOS_POR_JANELA = 20
buffer = []

print("Sistema IA Ativo!")
if lcd_ligado:
    lcd.clear()
    lcd.putstr("Pronto!")

while True:
    try:
        data = i2c_sensor.readfrom_mem(ADDR_SENSOR, 0x32, 6)
        x, y, z = ustruct.unpack('<hhh', data)
        buffer.append([x, y, z])

        if len(buffer) == PONTOS_POR_JANELA:

            # Filtro de repouso
            max_x = max(p[0] for p in buffer)
            min_x = min(p[0] for p in buffer)
            max_y = max(p[1] for p in buffer)
            min_y = min(p[1] for p in buffer)

            if (max_x - min_x) < 40 and (max_y - min_y) < 40:
                buffer = buffer[10:]
                time.sleep(0.05)
                continue

            # Preprocessing igual ao Colab
            ref_x, ref_y, ref_z = buffer[0]
            inputs = []
            for bx, by, bz in buffer:
                inputs.append((bx - ref_x) / 500.0)
                inputs.append((by - ref_y) / 500.0)
                inputs.append((bz - ref_z) / 500.0)

            probs = ai_puro.predict(inputs)
            idx = probs.index(max(probs))
            certeza = max(probs) * 100

            if certeza > 75.0 and LABELS[idx] != "Repouso":
                print("RECONHECIDO: {} ({:.0f}%)".format(LABELS[idx], certeza))
                if lcd_ligado:
                    lcd.clear()
                    lcd.putstr("GESTO:")
                    lcd.move_to(0, 1)
                    lcd.putstr("> " + LABELS[idx])
                    lcd.move_to(0, 2)
                    lcd.putstr("{:.0f}% confianca".format(certeza))

            buffer = buffer[10:]

    except OSError:
        pass

    time.sleep(0.05)