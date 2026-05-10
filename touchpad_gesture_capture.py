import time
import math
import sys

try:
    from pynput import mouse
except ImportError:
    print("Dependência em falta.")
    print("Instala com:")
    print("pip install pynput")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════
PONTOS_POR_JANELA = 30
DURACAO_CAPTURA = 3.0
ATRASO_LEITURA = 0.05

ESCALA_RACIO = 15.0
CLAMP_MAX = 500.0

# ═══════════════════════════════════════════════════════════
# CAPTURA DO RATO
# ═══════════════════════════════════════════════════════════
posicao_atual = [None, None]
amostras_raw = []

def on_move(x, y):
    """Callback chamado a cada movimento do rato."""
    if posicao_atual[0] is not None:
        dx = (x - posicao_atual[0]) * ESCALA_RACIO
        dy = (y - posicao_atual[1]) * ESCALA_RACIO

        dx = max(-CLAMP_MAX, min(CLAMP_MAX, dx))
        dy = max(-CLAMP_MAX, min(CLAMP_MAX, dy))

        amostras_raw.append((dx, dy))

    posicao_atual[0] = x
    posicao_atual[1] = y

def normalizar_dinamico(valores):
    """
    Normalização dinâmica baseada no intervalo real dos dados.
    """

    min_v = min(valores)
    max_v = max(valores)
    rang = max_v - min_v

    if rang < 1e-9:
        return [0.5] * len(valores)

    return [(v - min_v) / rang for v in valores]

def capturar_gesto():
    """Captura o gesto e retorna as amostras brutas."""

    global amostras_raw, posicao_atual

    amostras_raw = []
    posicao_atual = [None, None]

    print("\n" + "═" * 55)
    print("  CAPTURA DE GESTO PARA O WOKWI")
    print("═" * 55)
    print()
    print("  Vai ter 3 segundos de preparação...")
    print()

    for i in range(3, 0, -1):
        print(f"  Pronto em {i}...", end="\r")
        time.sleep(1)

    print()
    print("  A gravar movimento...")
    print(f"  (Duração: {DURACAO_CAPTURA} segundos)")
    print()

    listener = mouse.Listener(on_move=on_move)
    listener.start()

    inicio = time.time()

    while time.time() - inicio < DURACAO_CAPTURA:
        elapsed = time.time() - inicio

        progresso = int((elapsed / DURACAO_CAPTURA) * 20)
        barra = "█" * progresso + "░" * (20 - progresso)

        print(f"  [{barra}] {elapsed:.1f}s", end="\r")

        time.sleep(ATRASO_LEITURA)

    listener.stop()

    print()
    print()
    print("  Captura concluída.")

    return amostras_raw

def processar_amostras(amostras_raw):
    """
    Converte as amostras do rato em 30 pontos com x, y, z normalizados.
    """

    if len(amostras_raw) == 0:
        print("\n  Nenhum movimento detetado.")
        return None

    n = len(amostras_raw)

    if n < 2:
        print("\n  Movimento demasiado curto.")
        return None

    # Reamostragem para número fixo de pontos
    indices = [
        int(i * (n - 1) / (PONTOS_POR_JANELA - 1))
        for i in range(PONTOS_POR_JANELA)
    ]

    pontos_reamostrados = [amostras_raw[i] for i in indices]

    # Extrair eixos
    xs = [p[0] for p in pontos_reamostrados]
    ys = [p[1] for p in pontos_reamostrados]

    # Z simulado usando a variação da magnitude
    magnitudes = [
        math.sqrt(p[0]**2 + p[1]**2)
        for p in pontos_reamostrados
    ]

    zs = [0.0] + [
        magnitudes[i] - magnitudes[i - 1]
        for i in range(1, PONTOS_POR_JANELA)
    ]

    # Normalização dinâmica por eixo
    xs_norm = normalizar_dinamico(xs)
    ys_norm = normalizar_dinamico(ys)
    zs_norm = normalizar_dinamico(zs)

    # Formato esperado pelo modelo
    inputs = []

    for i in range(PONTOS_POR_JANELA):
        inputs.append(round(xs_norm[i], 4))
        inputs.append(round(ys_norm[i], 4))
        inputs.append(round(zs_norm[i], 4))

    return inputs

def formatar_saida(inputs):
    vals = ", ".join(f"{v:.4f}" for v in inputs)
    return f"[{vals}]"

def main():

    print()
    print("  Gestos suportados pelo modelo:")
    print("  Circulo   → move o rato em círculo")
    print("  Quadrado  → move o rato em forma de quadrado")
    print("  Triangulo → move o rato em forma de triângulo")
    print("  Repouso   → não mexas o rato")
    print()

    print("  Dica:")
    print("  - Faz movimentos amplos")
    print("  - Mantém mudanças de direção claras")
    print()

    while True:

        input("  Prima ENTER para iniciar uma nova captura (Ctrl+C para sair)...")

        amostras = capturar_gesto()

        inputs = processar_amostras(amostras)

        if inputs is None:
            continue

        if len(inputs) != PONTOS_POR_JANELA * 3:
            print(
                f"\n  Erro: esperados "
                f"{PONTOS_POR_JANELA * 3} valores, "
                f"obtidos {len(inputs)}"
            )
            continue

        inputs_str = formatar_saida(inputs)

        print()
        print("═" * 55)
        print("  Resultado — copia este array para o Wokwi:")
        print("═" * 55)
        print()

        print(inputs_str)

        print()
        print("═" * 55)
        print()

        # Estatísticas
        min_v = min(inputs)
        max_v = max(inputs)

        print("  Estatísticas:")
        print(f"  Amostras capturadas: {len(amostras)}")
        print(f"  Range dos valores: [{min_v:.3f}, {max_v:.3f}]")

        if max_v - min_v < 0.3:
            print("  Range reduzido — tenta fazer um gesto com maior amplitude.")
        else:
            print("  Range OK.")

        print()

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\n\n  Programa terminado.")