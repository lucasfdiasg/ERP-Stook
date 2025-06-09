import os

# =======================================================
# Função para limpar o terminal (tela)
# -------------------------------------------------------
# Compatível com:
# - Windows (comando: cls)
# - Linux/MacOS (comando: clear)
# =======================================================
def limpar_tela():
    """Limpa o terminal de forma compatível com Windows e Unix."""
    os.system('cls' if os.name == 'nt' else 'clear')


# =======================================================
# Função para exibir o cabeçalho padrão do sistema
# -------------------------------------------------------
# Inclui o nome do sistema formatado centralizado
# Também executa a limpeza da tela antes
# =======================================================
def exibir_cabecalho():
    """Exibe o cabeçalho padrão do sistema."""
    limpar_tela()
    print("=" * 50)
    print("|  S T O O K   -   G E R E N C I A D O R   V2.1  |".center(50))
    print("=" * 50)


# =======================================================
# Função para pausar a execução do programa
# -------------------------------------------------------
# Útil após mensagens ou blocos importantes,
# para aguardar o usuário antes de continuar.
# =======================================================
def pausar():
    """Aguarda o usuário pressionar ENTER para continuar."""
    input("\nPressione ENTER para continuar...")
