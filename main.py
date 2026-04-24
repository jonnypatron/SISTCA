import machine
import time
import ustruct
import gc         # Adiciona isto

gc.collect()      # Limpa a memória!
import ai_puro    # Agora sim, carrega a IA com espaço livre

# Configuração do Sensor
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
ADDR = 0x53

try:
    i2c.writeto_mem(ADDR, 0x2D, b'\x08')
except OSError:
    pass

# A ORDEM EXATA QUE SAIU NO COLAB
LABELS = ["Circulo", "Quadrado", "Repouso", "Triangulo"]

PONTOS_POR_JANELA = 30
ATRASO_LEITURA = 0.05
buffer = []

print("Sistema Edge AI Iniciado! Aguardando gestos...")

while True:
    try:
        # Lê o sensor
        data = i2c.readfrom_mem(ADDR, 0x32, 6)
        x, y, z = ustruct.unpack('<hhh', data)
        
        # Normalização matemática (exatamente igual à do Colab!)
        nx = (x - (-500.0)) / (500.0 - (-500.0))
        ny = (y - (-500.0)) / (500.0 - (-500.0))
        nz = (z - (-500.0)) / (500.0 - (-500.0))
        
        # Adiciona à janela de tempo
        buffer.append([nx, ny, nz])
        
        # Quando a janela encher com 20 leituras (1 segundo de movimento)
        # Quando a janela encher com 20 leituras (1 segundo de movimento)
        if len(buffer) == PONTOS_POR_JANELA:
            
            # Achata a lista para 60 valores
            inputs = []
            for ponto in buffer:
                inputs.extend(ponto)
                
            # A Inteligência Artificial faz a previsão!
            probabilidades = ai_puro.predict(inputs)
            classe_id = probabilidades.index(max(probabilidades))
            certeza = max(probabilidades) * 100
            
            # ---> O NOSSO RAIO-X (IMPRIME TUDO O QUE A IA PENSA) <---
            print(f"[DEBUG] Lendo: {LABELS[classe_id]} com {certeza:.1f}% de certeza")
            
            # Só imprime o gesto final se tiver > 80% e NÃO for ruído
            if certeza > 60.0 and LABELS[classe_id] != "Repouso":
                print(f"🏆 GESTO RECONHECIDO: {LABELS[classe_id]} ({certeza:.1f}%) 🏆")
            
            # Desliza a janela
            buffer = buffer[5:]
            
    except OSError:
        # Se houver mau contacto no fio, ignora e tenta no próximo ciclo!
        pass
        
    time.sleep(ATRASO_LEITURA)