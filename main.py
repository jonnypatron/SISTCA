import machine
import time
import ustruct
import gc

gc.collect()
import ai_puro

# --- INÍCIO SEGURO (Espera 2s para não crashar) ---
time.sleep(2)

i2c_sensor = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADDR_SENSOR = 0x53

try: i2c_sensor.writeto_mem(ADDR_SENSOR, 0x2D, b'\x08')
except OSError: pass

# --- TENTA LIGAR O LCD ---
lcd_ligado = False
try:
    from machine_i2c_lcd import I2cLcd
    i2c_lcd = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=400000)
    try: lcd = I2cLcd(i2c_lcd, 0x27, 4, 20); lcd_ligado = True
    except: lcd = I2cLcd(i2c_lcd, 0x3f, 4, 20); lcd_ligado = True
except: pass

LABELS = ["Circulo", "Quadrado", "Repouso", "Triangulo"] # VERIFICA SE É A ORDEM DO COLAB
PONTOS_POR_JANELA = 20 
buffer = []

print("🚀 Sistema IA Ativo! Podes mover o sensor em qualquer posição.")

while True:
    try:
        data = i2c_sensor.readfrom_mem(ADDR_SENSOR, 0x32, 6)
        x, y, z = ustruct.unpack('<hhh', data)
        buffer.append([x, y, z]) # Guarda cru!
        
        if len(buffer) == PONTOS_POR_JANELA:
            # 1. Filtro Anti-Ruído: Calcula a variação máxima
            max_x = max([p[0] for p in buffer]); min_x = min([p[0] for p in buffer])
            max_y = max([p[1] for p in buffer]); min_y = min([p[1] for p in buffer])
            
            # Se a mão mal se mexeu, é Repouso, limpa e salta!
            if (max_x - min_x) < 40 and (max_y - min_y) < 40:
                print("--- Repouso ---")
                buffer = buffer[10:]
                time.sleep(0.05)
                continue

            # 2. A MÁGICA: Subtrair o primeiro ponto (Referência)
            ref_x, ref_y, ref_z = buffer[0]
            
            inputs = []
            for bx, by, bz in buffer:
                inputs.append((bx - ref_x) / 500.0)
                inputs.append((by - ref_y) / 500.0)
                inputs.append((bz - ref_z) / 500.0)
                
            probabilidades = ai_puro.predict(inputs)
            classe_id = probabilidades.index(max(probabilidades))
            certeza = max(probabilidades) * 100
            
            if certeza > 75.0 and LABELS[classe_id] != "Repouso":
                msg = f"{LABELS[classe_id]} ({certeza:.0f}%)"
                print(f"⭐ RECONHECIDO: {msg} ⭐")
                
                if lcd_ligado:
                    lcd.clear()
                    lcd.putstr(" GESTO: ")
                    lcd.move_to(0, 1)
                    lcd.putstr(f"> {LABELS[classe_id]}")
            
            buffer = buffer[10:] # Salta 10 pontos
            
    except OSError:
        pass
        
    time.sleep(0.05)