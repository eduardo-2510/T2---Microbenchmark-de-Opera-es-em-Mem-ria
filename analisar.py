from comum import *

dados = {
    "Windows": validar_csv("memoria_windows_original.csv"),
    "Linux": validar_csv("memoria_linux_original.csv")
}
with open("memoria_processada.csv", "w", encoding="utf-8", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["sistema"] + CABECALHO)
    for sistema, registros in dados.items():
        for registro in registros:
            escritor.writerow([sistema] + [registro[c] for c in CABECALHO])

resumo = {}
for sistema, registros in dados.items():
    for mb in TAMANHOS:
        for operacao in OPERACOES:
            valores = [r[operacao] for r in registros if r["bloco_MB"] == mb]
            media = sum(valores) / len(valores)
            desvio = (sum((v-media)**2 for v in valores) / (len(valores)-1))**0.5
            resumo[(sistema, operacao, mb)] = (media, desvio)

comparacao = []
with open("tabela_comparativa.csv", "w", encoding="utf-8", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["operacao", "bloco_MB", "n_por_sistema", "media_windows_ms",
                       "desvio_windows_ms", "media_linux_ms", "desvio_linux_ms",
                       "diferenca_windows_menos_linux_ms", "menor_media"])
    for operacao, nome in OPERACOES.items():
        print("\n" + nome + " | MB | Windows média ± DP | Linux média ± DP | W-L (ms)")
        for mb in TAMANHOS:
            mw, dw = resumo[("Windows", operacao, mb)]
            ml, dl = resumo[("Linux", operacao, mb)]
            menor = "Windows" if mw < ml else "Linux" if ml < mw else "Empate"
            linha = [nome, mb, 100, mw, dw, ml, dl, mw-ml, menor]
            comparacao.append(linha)
            escritor.writerow(linha)
            print(f"{mb:4} | {mw:.6f} ± {dw:.6f} | {ml:.6f} ± {dl:.6f} | {mw-ml:.6f}")
print("\nCriados memoria_processada.csv e tabela_comparativa.csv; originais preservados.")

def grafico_svg(operacao, nome):
    largura, altura = 900, 520
    esquerda, direita, topo, base = 100, 860, 60, 420
    limite = max(resumo[(s, operacao, mb)][0] + resumo[(s, operacao, mb)][1]
                 for s in dados for mb in TAMANHOS) * 1.1 or 1
    def x(mb): return esquerda + (mb-100)/900 * (direita-esquerda)
    def y(tempo): return base - tempo/limite * (base-topo)
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">',
              '<rect width="100%" height="100%" fill="white"/>',
              f'<text x="100" y="28" font-family="sans-serif" font-size="20">{nome}: média ± desvio padrão amostral</text>']
    for i in range(6):
        valor = limite*i/5
        yy = y(valor)
        partes += [f'<line x1="{esquerda}" y1="{yy}" x2="{direita}" y2="{yy}" stroke="#ddd"/>',
                   f'<text x="90" y="{yy+4}" text-anchor="end" font-size="12">{valor:.3f}</text>']
    for mb in TAMANHOS:
        partes.append(f'<text x="{x(mb)}" y="445" text-anchor="middle" font-size="12">{mb}</text>')
    for sistema, cor, legenda_x in [("Windows", "#2563eb", 280), ("Linux", "#dc2626", 510)]:
        pontos = " ".join(f"{x(mb)},{y(resumo[(sistema,operacao,mb)][0])}" for mb in TAMANHOS)
        partes.append(f'<polyline points="{pontos}" fill="none" stroke="{cor}" stroke-width="2"/>')
        for mb in TAMANHOS:
            media, dp = resumo[(sistema,operacao,mb)]
            xx, superior, inferior = x(mb), y(media+dp), y(max(0,media-dp))
            partes += [f'<path d="M {xx} {superior} V {inferior} M {xx-4} {superior} H {xx+4} M {xx-4} {inferior} H {xx+4}" stroke="{cor}"/>',
                       f'<circle cx="{xx}" cy="{y(media)}" r="3" fill="{cor}"/>']
        partes.append(f'<text x="{legenda_x}" y="500" fill="{cor}" font-size="15">{sistema}</text>')
    partes += ['<text x="450" y="475" text-anchor="middle" font-size="14">Tamanho de bloco (MB, conforme material)</text>',
               '<text x="20" y="240" transform="rotate(-90 20 240)" text-anchor="middle" font-size="14">Tempo (ms)</text>', '</svg>']
    caminho = f"grafico_{operacao}.svg"
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(partes))
    print("Criado:", caminho)

for operacao, nome in OPERACOES.items():
    grafico_svg(operacao, nome)
