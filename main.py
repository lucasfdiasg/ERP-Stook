import os
import time
from interface.menus import menu_principal, submenu_produtos, criar_engradado, menu_armazenar_engradado


# Limpa a tela para manter interface limpa
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Exibe o cabeçalho principal do sistema
from utils.exibicao import exibir_cabecalho

def exibir_cabecalho_local():
    limpar_tela()
    print("=" * 50)
    print("|  S T O O K   -   G E R E N C I A D O R   V1.0  |".center(50))
    print("=" * 50)

# Espera confirmação do usuário
def pausar(mensagem="Pressione ENTER para continuar..."):
    input(f"\n{mensagem}")

# Loop principal do sistema
def executar():
    while True:
        try:
            exibir_cabecalho_local()
            opcao = menu_principal()

            if opcao == '1':
                submenu_produtos()
            elif opcao == '2':
                criar_engradado()
            elif opcao == '3':
                menu_armazenar_engradado()
            elif opcao == '0':
                print("\nEncerrando o sistema... Até logo! 👋")
                time.sleep(1)
                break
            else:
                print("\n[!] Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um erro inesperado: {e}")
        pausar()


if __name__ == "__main__":
    executar()
