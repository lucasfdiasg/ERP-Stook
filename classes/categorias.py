import json
import os
from utils.exibicao import exibir_cabecalho

# Caminho padrão para o arquivo de categorias
CAMINHO_CATEGORIAS = "database/categorias.json"

# -------------------------------------------
# Função para carregar categorias do arquivo JSON
# Retorna um dicionário com {chave_interna: nome_visivel}
# -------------------------------------------
def carregar_categorias():
    if not os.path.exists(CAMINHO_CATEGORIAS):
        return {}  # Se o arquivo não existir, retorna dicionário vazio
    with open(CAMINHO_CATEGORIAS, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------------------
# Função para salvar o dicionário de categorias no JSON
# -------------------------------------------
def salvar_categorias(categorias):
    with open(CAMINHO_CATEGORIAS, "w", encoding="utf-8") as f:
        json.dump(categorias, f, indent=4, ensure_ascii=False)

# -------------------------------------------
# Menu interativo para gerenciar categorias:
# adicionar, renomear, remover ou voltar ao menu principal
# -------------------------------------------
def gerenciar_categorias():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_cabecalho()
        print("=" * 50)
        print("GERENCIAR CATEGORIAS".center(50))
        print("=" * 50)

        # Carrega as categorias atuais
        categorias = carregar_categorias()

        # Exibe categorias cadastradas (se houver)
        if not categorias:
            print("\nNenhuma categoria cadastrada ainda.")
        else:
            print("\nCategorias cadastradas:")
            for key, nome in categorias.items():
                print(f"- {key}: {nome}")

        # Menu de opções
        print("\n1. Adicionar categoria")
        print("2. Renomear categoria")
        print("3. Remover categoria")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        # -------------------------------------------
        # [1] Adiciona nova categoria
        # -------------------------------------------
        if opcao == "1":
            nova = input("Nome da nova categoria: ").strip()
            chave = nova.lower().replace(" ", "_")  # Cria chave única
            if chave not in categorias:
                categorias[chave] = nova  # Salva no dicionário
                salvar_categorias(categorias)
                print("✅ Categoria adicionada.")
            else:
                print("⚠️ Categoria já existe.")

        # -------------------------------------------
        # [2] Renomeia uma categoria existente
        # -------------------------------------------
        elif opcao == "2":
            chave = input("Chave interna da categoria (ex: higiene): ").strip()
            if chave in categorias:
                novo_nome = input("Novo nome visível: ").strip()
                categorias[chave] = novo_nome
                salvar_categorias(categorias)
                print("✅ Categoria atualizada.")
            else:
                print("⚠️ Categoria não encontrada.")

        # -------------------------------------------
        # [3] Remove uma categoria existente
        # -------------------------------------------
        elif opcao == "3":
            chave = input("Chave interna da categoria: ").strip()
            if chave in categorias:
                del categorias[chave]
                salvar_categorias(categorias)
                print("✅ Categoria removida.")
            else:
                print("⚠️ Categoria não encontrada.")

        # -------------------------------------------
        # [0] Voltar ao menu anterior
        # -------------------------------------------
        elif opcao == "0":
            break

        # -------------------------------------------
        # Opção inválida
        # -------------------------------------------
        else:
            print("⚠️ Opção inválida.")

        input("\nPressione ENTER para continuar...")
