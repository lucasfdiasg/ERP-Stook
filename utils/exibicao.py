import os

def limpar_tela():
    """Limpa o terminal de forma compatível com Windows e Unix."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho():
    """Exibe o cabeçalho padrão do sistema."""
    limpar_tela()
    print("=" * 50)
    print("|  S T O O K   -   G E R E N C I A D O R   V1.0  |".center(50))
    print("=" * 50)

def pausar():
    """Aguarda o usuário pressionar ENTER para continuar."""
    input("\nPressione ENTER para continuar...")
