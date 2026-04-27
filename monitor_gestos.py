import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configure the serial port (Workstation side)
# Ensure the Raspberry Pi Pico is connected to 'COM3' at 115200 baud
ser = serial.Serial('COM3', 115200)

x_data, y_data = [], []

# Setup the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], 'ro-', markersize=3)
ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
ax.set_title("Real-Time Sensor Trajectory (X vs Y)")
ax.set_xlabel("X-Axis Acceleration")
ax.set_ylabel("Y-Axis Acceleration")
ax.grid(True)

def update(frame):
    try:
        if ser.in_waiting > 0:
            # Read and decode the incoming data from the Pico
            line_str = ser.readline().decode('utf-8').strip()
            if "|" in line_str:
                parts = [float(p.strip()) for p in line_str.split("|")]
                x_data.append(parts[0])
                y_data.append(parts[1])

                # Maintain the last 50 data points for visualizationn
                if len(x_data) > 50:
                    x_data.pop(0)
                    y_data.pop(0)

                line.set_data(x_data, y_data)
    except Exception:
        pass
    return line,

# Animate the plot at a 10ms interval
ani = FuncAnimation(fig, update, interval=10, blit=True)
plt.show()