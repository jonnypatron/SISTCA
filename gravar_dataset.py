import serial
import csv

# Configuração
porta = 'COM3'
label = "triangulo" # Muda para "quadrado" ou "repouso" conforme o que fores gravar
arquivo_nome = f"dados_{label}.csv"

ser = serial.Serial(porta, 115200, timeout=1)
print(f"A gravar {label}... Faz o gesto repetidamente! (Ctrl+C para parar)")

try:
    with open(arquivo_nome, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z", "label"]) # Cabeçalho
        
        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode('utf-8', errors='ignore').strip()
                if "|" in linha:
                    parts = [p.strip() for p in linha.split("|")]
                    if len(parts) == 3:
                        writer.writerow([parts[0], parts[1], parts[2], label])
                        # Feedback visual rápido
                        print(f"Ponto capturado: {parts}", end='\r')
except KeyboardInterrupt:
    print(f"\nGravação de {label} terminada com sucesso!")
    ser.close()