from classes.estoque import Estoque
from classes.engradado import Engradado
from utils.exibicao import limpar_tela, pausar
import string

def armazenar_engradado_no_estoque(estoque: Estoque, engradado: Engradado):
    limpar_tela()
    print("ARMAZENAR ENGRADADO NO ESTOQUE".center(50, "="))

    print(f"Produto do engradado: {engradado.codigo_produto}")
    print(f"Lote: {engradado.lote} | Validade: {engradado.validade}")

    # Mostrar endereços válidos
    print("\nEndereços disponíveis:")
    for linha in range(5):
        for coluna in range(8):
            posicao = f"{string.ascii_uppercase[linha]}{coluna+1}"
            pilha = estoque.matriz[linha][coluna]
            topo = pilha.topo()
            quantidade = len(pilha.pilha)

            if quantidade < 5 and (topo is None or topo.codigo_produto == engradado.codigo_produto):
                print(f"  - {posicao} (ocupado: {quantidade})")

    destino = input("\nDigite o endereço onde deseja armazenar (ex: B3): ").strip().upper()
    if len(destino) < 2:
        print("Endereço inválido.")
        pausar()
        return

    linha = ord(destino[0]) - ord('A')
    try:
        coluna = int(destino[1:]) - 1
    except ValueError:
        print("Endereço inválido.")
        pausar()
        return

    if not (0 <= linha < 5 and 0 <= coluna < 8):
        print("Endereço fora da matriz.")
        pausar()
        return

    pilha = estoque.matriz[linha][coluna]
    topo = pilha.topo()

    if len(pilha.pilha) >= 5:
        print("Essa pilha já está cheia (máx. 5 engradados).")
    elif topo is not None and topo.codigo_produto != engradado.codigo_produto:
        print("Essa pilha contém engradados de outro produto.")
    else:
        pilha.empilhar(engradado)
        print(f"Engradado armazenado com sucesso em {destino}.")

    pausar()
