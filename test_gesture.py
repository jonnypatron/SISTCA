# test_gesture.py — usar no Wokwi
# =========================================================
# 1. Corre o ficheiro touchpad_gesture_capture.py no teu PC
# 2. Copia o array de inputs apresentado no terminal
# 3. Substitui o array abaixo pelo array gerado
# 4. No Wokwi, define este ficheiro como ficheiro principal
# 5. Corre a simulação para obter a classificação do gesto
# =========================================================

import ai_puro

LABELS = ["Circulo", "Quadrado", "Repouso", "Triangulo"]

# Substitui este array pelo array gerado pelo script
inputs = [0.2021, 1.0000, 0.4792, 0.2953, 0.3800, 0.0148, 0.2798, 0.3950, 0.4860, 0.0466, 0.8900, 0.9433, 0.2642, 0.5000, 0.0000, 0.1399, 0.5000, 0.6376, 0.3886, 0.3650, 0.2578, 0.4663, 0.4400, 0.3467, 0.4819, 0.5150, 0.4174, 0.6062, 0.5150, 0.6190, 0.8238, 0.5000, 0.7551, 1.0000, 0.4700, 0.7047, 0.9326, 0.4700, 0.3936, 1.0000, 0.3200, 0.6051, 1.0000, 0.3650, 0.4614, 0.8394, 0.4400, 0.2579, 0.7461, 0.4700, 0.3559, 0.5596, 0.5000, 0.2394, 0.4974, 0.5000, 0.4000, 0.2487, 0.3200, 0.8396, 0.0000, 0.0000, 1.0000, 0.2021, 0.0000, 0.3280, 0.0311, 0.0000, 0.6039, 0.2487, 0.1100, 0.1988, 0.2798, 0.1850, 0.3739, 0.3264, 0.2600, 0.3638, 0.2953, 0.2600, 0.5016, 0.4819, 0.5450, 0.1427, 0.4819, 0.5150, 0.4396, 0.4819, 0.5300, 0.4990]

# Verificação do tamanho do array
if len(inputs) != 90:
    print(f"Erro: esperados 90 valores, foram recebidos {len(inputs)}")
else:
    probs = ai_puro.predict(inputs)
    idx = probs.index(max(probs))
    certeza = max(probs) * 100

    print("=" * 40)
    print("Resultado do gesto")
    print("=" * 40)
    print(f"Gesto: {LABELS[idx]}")
    print(f"Certeza: {certeza:.1f}%")
    print()
    print("Probabilidades:")

    for i, (label, prob) in enumerate(zip(LABELS, probs)):
        barra = "#" * int(prob * 20)
        marcador = " <- selecionado" if i == idx else ""
        print(f"{label:10s}: {prob * 100:5.1f}% {barra}{marcador}")

    print("=" * 40)