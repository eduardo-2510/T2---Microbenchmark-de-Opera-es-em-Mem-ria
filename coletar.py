from comum import *

def coletar(sistema):
    if sistema not in ("Windows", "Linux"):
        raise ValueError("Informe Windows ou Linux")
    caminho = f"memoria_{sistema.lower()}_original.csv"
    with open(caminho, "x", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(CABECALHO)
        for mb in TAMANHOS:
            bloco_bytes = mb * 1024 * 1024
            for teste in range(1, REPETICOES + 1):
                padrao = b"\xAA" * bloco_bytes  # preparação fora da medição
                t0 = time.perf_counter_ns()
                bloco = bytearray(bloco_bytes)
                t1 = time.perf_counter_ns()
                t2 = time.perf_counter_ns()
                bloco[:] = padrao
                t3 = time.perf_counter_ns()
                t4 = time.perf_counter_ns()
                soma = sum(bloco)
                t5 = time.perf_counter_ns()
                t6 = time.perf_counter_ns()
                bloco.clear()
                del bloco
                t7 = time.perf_counter_ns()
                del padrao
                tempos = [(t1-t0)/1_000_000, (t3-t2)/1_000_000,
                          (t5-t4)/1_000_000, (t7-t6)/1_000_000]
                escritor.writerow([mb, teste] + [f"{t:.6f}" for t in tempos])
            print(f"{sistema}: concluído bloco de {mb} MB")
    validar_csv(caminho)
    return caminho


if __name__ == "__main__":
    sistema = input("Sistema em execução (Windows ou Linux): ").strip()
    coletar(sistema)
