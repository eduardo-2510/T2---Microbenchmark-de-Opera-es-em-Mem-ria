import time

#Medir tempo 

inicio = time.perf_counter_ns()

# operação cujo tempo queremos observar
soma = sum(range(1_000_000)) # soma os números de 0 a 999.999

fim = time.perf_counter_ns()

delta_ns = fim - inicio
delta_ms = delta_ns / 1_000_000

print("Tempo em nanossegundos:", delta_ns)
print(f"Tempo em milissegundos: {delta_ms:.6f} ms")

#Fim de medição de tempo

#Converter tamanho de bloco de memória de MB para bytes
tamanho = 1024  # bytes; tamanho para demonstração #1Kb

t0 = time.perf_counter_ns() #tempo inicial
bloco = bytearray(tamanho) #alocando memória
t1 = time.perf_counter_ns() # tempo final

alloc_ms = (t1 - t0) / 1_000_000

print("Quantidade de bytes:", len(bloco))
print(f"Tempo de alocação: {alloc_ms:.6f} ms")
print(list(bloco))

#Escrita
bloco_teste = bytearray(10)
padrao = b'\xAA' * len(bloco_teste)  # dez bytes; preparado fora da medição

t2 = time.perf_counter_ns()
bloco_teste[:] = padrao
t3 = time.perf_counter_ns()

write_ms = (t3 - t2) / 1_000_000

print(f"Tempo de escrita: {write_ms:.6f} ms")
print("Tamanho após a escrita:", len(bloco_teste))  # 10

#Leitura
bloco = bytearray([1, 2, 3, 4, 5])

t4 = time.perf_counter_ns()
soma = sum(bloco)
t5 = time.perf_counter_ns()

read_ms = (t5 - t4) / 1_000_000

print("Soma calculada:", soma)
print(f"Tempo de leitura: {read_ms:.6f} ms")

#Liberação de memória
bloco = bytearray(10)

t6 = time.perf_counter_ns()
bloco.clear()
del bloco
t7 = time.perf_counter_ns()

free_ms = (t7 - t6) / 1_000_000
print(f"Tempo medido: {free_ms:.6f} ms")