import os
import time
from interface.menus import menu_principal,\
                            submenu_produtos,\
                            criar_engradado,\
                            menu_armazenar_engradado, \
                            exibir_cabecalho, \
                            pausar, visualizar_estoque_detalhado, remover_engradado_do_estoque, submenu_pedidos


# Loop principal do sistema
def executar():
    while True:
        try:
            exibir_cabecalho()
            opcao = menu_principal()

            if opcao == '1':
                submenu_produtos()
            elif opcao == '2':
                criar_engradado()
            elif opcao == '3':
                menu_armazenar_engradado()
            elif opcao == '4':
                visualizar_estoque_detalhado()
            elif opcao == '5':
                remover_engradado_do_estoque()      
            elif opcao == '6':
                submenu_pedidos()
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
