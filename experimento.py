import csv
import time

# FUNÇÕES DE OPERAÇÕES DE MEMÓRIA

def alocacao(block_size):
    return bytearray(block_size)

def escrita(bloco):
    padrao = b'\xAA' * len(bloco)
    bloco[:] = padrao

def leitura(bloco):
    return sum(bloco)

def liberacao(bloco):
    bloco.clear()
    del bloco

# --- FUNÇÃO PRINCIPAL DO EXPERIMENTO ---

def PERFORM_TESTS(log_file, num_testes=100):
    # Configurações de tamanho (de 100MB até 1000MB com passo de 100MB)
    MIN_BLOCK_SIZE = 100 * 1024 * 1024  # 100 MB em bytes
    MAX_BLOCK_SIZE = 1000 * 1024 * 1024 # 1000 MB em bytes
    BLOCK_STEP = 100 * 1024 * 1024     # 100 MB em bytes

    resultados = []
    print("Iniciando o microbenchmark de memória...")

    # Laço externo: tamanho de bloco
    for block_size in range(MIN_BLOCK_SIZE, MAX_BLOCK_SIZE + BLOCK_STEP, BLOCK_STEP):
        block_size_mb = block_size // (1024 * 1024)
        print(f"Executando para bloco de {block_size_mb} MB...")

        # Laço interno: ensaios / repetições
        for test_num in range(1, num_testes + 1):
            
            # 1. Alocação
            t0 = time.perf_counter_ns()
            bloco = alocacao(block_size)
            t1 = time.perf_counter_ns()
            allocation_time_ms = (t1 - t0) / 1_000_000

            # 2. Escrita
            t2 = time.perf_counter_ns()
            escrita(bloco)
            t3 = time.perf_counter_ns()
            write_time_ms = (t3 - t2) / 1_000_000

            # 3. Leitura
            t4 = time.perf_counter_ns()
            soma_leitura = leitura(bloco)
            t5 = time.perf_counter_ns()
            read_time_ms = (t5 - t4) / 1_000_000

            # 4. Liberação
            t6 = time.perf_counter_ns()
            liberacao(bloco)
            t7 = time.perf_counter_ns()
            free_time_ms = (t7 - t6) / 1_000_000

            # Acumula as medições na lista
            resultados.append({
                "block_MB": block_size_mb,
                "teste": test_num,
                "alloc_ms": allocation_time_ms,
                "write_ms": write_time_ms,
                "read_ms": read_time_ms,
                "free_ms": free_time_ms
            })

    # Persistência no arquivo CSV apenas no final do teste
    print(f"\nSalvando os dados no arquivo CSV: {log_file}...")
    
    colunas = [
        "block_MB",
        "teste",
        "alloc_ms",
        "write_ms",
        "read_ms",
        "free_ms"
    ]

    with open(log_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(resultados)

    print("Concluído com sucesso!")

# Execução do experimento
if __name__ == "__main__":
    sistema = input("Digite o Sistema Operacional (ex: Windows, Linux): ")
    nome_arquivo = f"{sistema}_results.csv"
    PERFORM_TESTS(nome_arquivo, num_testes=100)