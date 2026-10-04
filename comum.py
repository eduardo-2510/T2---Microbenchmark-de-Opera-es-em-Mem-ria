import csv
import time

TAMANHOS = list(range(100, 1001, 100))
REPETICOES = 100
CABECALHO = ["bloco_MB", "teste", "alloc_ms", "write_ms", "read_ms", "free_ms"]
OPERACOES = {"alloc_ms": "Alocação", "write_ms": "Escrita", "read_ms": "Leitura", "free_ms": "Liberação"}

def validar_csv(caminho):
    registros = []
    identificadores = set()
    with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.reader(arquivo)
        if next(leitor, None) != CABECALHO:
            raise ValueError(f"{caminho}: cabeçalho incorreto")
        for numero, linha in enumerate(leitor, start=2):
            if len(linha) != 6:
                raise ValueError(f"{caminho}, linha {numero}: esperadas seis colunas")
            try:
                mb, teste = int(linha[0]), int(linha[1])
                tempos = [float(valor) for valor in linha[2:]]
            except ValueError:
                raise ValueError(f"{caminho}, linha {numero}: tipos inválidos")
            if mb not in TAMANHOS or teste not in range(1, REPETICOES + 1):
                raise ValueError(f"{caminho}, linha {numero}: tamanho ou teste fora do previsto")
            chave = (mb, teste)
            if chave in identificadores:
                raise ValueError(f"{caminho}, linha {numero}: identificador duplicado {chave}")
            if any(not (0 <= tempo < float("inf")) for tempo in tempos):
                raise ValueError(f"{caminho}, linha {numero}: tempo negativo, infinito ou NaN")
            identificadores.add(chave)
            registros.append(dict(zip(CABECALHO, [mb, teste] + tempos)))
    esperados = {(mb, t) for mb in TAMANHOS for t in range(1, REPETICOES + 1)}
    if len(registros) != 1000 or identificadores != esperados:
        raise ValueError(f"{caminho}: cobertura incompleta; {len(registros)} registros")
    print(f"APROVADO: {caminho} — 1.000 registros, dez tamanhos, 100 testes por tamanho")
    return registros
