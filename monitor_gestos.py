import serial
import matplotlib.pyplot as plt

try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
    print("Conectado à COM3. À espera de dados...")
except Exception as e:
    print(f"Erro ao abrir porta: {e}")
    exit()

plt.ion()
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], 'ro-', markersize=3)

ax.set_xlim(-500, 500) 
ax.set_ylim(-500, 500)
ax.grid(True)

while True:
    if ser.in_waiting > 0:
        raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
        
        print(f"Recebi: {raw_data}") 
        
        if "|" in raw_data:
            try:
                parts = [float(p.strip()) for p in raw_data.split("|")]
                x_data.append(parts[0])
                y_data.append(parts[1])
                
                if len(x_data) > 30:
                    x_data.pop(0)
                    y_data.pop(0)
                
                line.set_data(x_data, y_data)
                plt.draw()
                plt.pause(0.001)
            except ValueError:
                continue
    else:
        plt.pause(0.01)