import machine
import time
import ustruct
import gc

gc.collect()
import ai_puro

# --- INÍCIO SEGURO ---
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

# --- CONFIGURAÇÃO DO CHALLENGE ---
# Substitui pelas letras que treinaste no Colab. O "Repouso" deve estar na lista.
LABELS = ["J", "O", "A", "Repouso"] 
PONTOS_POR_JANELA = 20 
buffer = []

# Variáveis de Estado
palavra_atual = ""
letra_detetada_agora = None
esta_a_escrever = False

print("🚀 Air-Writer Ativo!")
print("Instruções: Faz o gesto de uma letra e volta ao REPOUSO para confirmar.")

while True:
    try:
        data = i2c_sensor.readfrom_mem(ADDR_SENSOR, 0x32, 6)
        x, y, z = ustruct.unpack('<hhh', data)
        buffer.append([x, y, z])
        
        if len(buffer) == PONTOS_POR_JANELA:
            # 1. Filtro Anti-Ruído
            max_x = max([p[0] for p in buffer]); min_x = min([p[0] for p in buffer])
            max_y = max([p[1] for p in buffer]); min_y = min([p[1] for p in buffer])
            
            # Cálculo de "Repouso" Manual (Variação baixa)
            eh_repouso_manual = (max_x - min_x) < 40 and (max_y - min_y) < 40

            # 2. Inferência de IA
            ref_x, ref_y, ref_z = buffer[0]
            inputs = []
            for bx, by, bz in buffer:
                inputs.append((bx - ref_x) / 500.0)
                inputs.append((by - ref_y) / 500.0)
                inputs.append((bz - ref_z) / 500.0)
                
            probabilidades = ai_puro.predict(inputs)
            classe_id = probabilidades.index(max(probabilidades))
            certeza = max(probabilidades)
            label_ia = LABELS[classe_id]

            # --- LÓGICA DO CHALLENGE (MÁQUINA DE ESTADOS) ---
            
            # A. Detetou uma Letra com confiança alta
            if label_ia != "Repouso" and certeza > 0.85:
                letra_detetada_agora = label_ia
                esta_a_escrever = True
                print(f"✍️ A desenhar: {label_ia}...", end="\r")

            # B. Voltou ao Repouso (IA ou Manual) após ter escrito algo
            elif (label_ia == "Repouso" or eh_repouso_manual) and esta_a_escrever:
                palavra_atual += letra_detetada_agora
                esta_a_escrever = False
                
                # Feedback no Terminal (Limpa e mostra a palavra)
                print("\n" + "="*20)
                print(f"📝 PALAVRA: {palavra_atual}")
                print("="*20)
                
                # Feedback no LCD
                if lcd_ligado:
                    lcd.clear()
                    lcd.putstr("Air-Writer:")
                    lcd.move_to(0, 1)
                    lcd.putstr(f"> {palavra_atual}")

            buffer = buffer[10:] 
            
    except OSError:
        pass
        
    time.sleep(0.05)