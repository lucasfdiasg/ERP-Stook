import json
import os
from utils.exibicao import exibir_cabecalho


CAMINHO_CATEGORIAS = "database/categorias.json"

def carregar_categorias():
    if not os.path.exists(CAMINHO_CATEGORIAS):
        return {}
    with open(CAMINHO_CATEGORIAS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_categorias(categorias):
    with open(CAMINHO_CATEGORIAS, "w", encoding="utf-8") as f:
        json.dump(categorias, f, indent=4, ensure_ascii=False)

def gerenciar_categorias():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        exibir_cabecalho()
        print("=" * 50)
        print("GERENCIAR CATEGORIAS".center(50))
        print("=" * 50)

        categorias = carregar_categorias()
        if not categorias:
            print("\nNenhuma categoria cadastrada ainda.")

        else:
            print("\nCategorias cadastradas:")
            for key, nome in categorias.items():
                print(f"- {key}: {nome}")

        print("\n1. Adicionar categoria")
        print("2. Renomear categoria")
        print("3. Remover categoria")
        print("0. Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            nova = input("Nome da nova categoria: ").strip()
            chave = nova.lower().replace(" ", "_")
            if chave not in categorias:
                categorias[chave] = nova
                salvar_categorias(categorias)
                print("✅ Categoria adicionada.")
            else:
                print("⚠️ Categoria já existe.")
        elif opcao == "2":
            chave = input("Chave interna da categoria (ex: higiene): ").strip()
            if chave in categorias:
                novo_nome = input("Novo nome visível: ").strip()
                categorias[chave] = novo_nome
                salvar_categorias(categorias)
                print("✅ Categoria atualizada.")
            else:
                print("⚠️ Categoria não encontrada.")
        elif opcao == "3":
            chave = input("Chave interna da categoria: ").strip()
            if chave in categorias:
                del categorias[chave]
                salvar_categorias(categorias)
                print("✅ Categoria removida.")
            else:
                print("⚠️ Categoria não encontrada.")
        elif opcao == "0":
            break
        else:
            print("⚠️ Opção inválida.")

        input("\nPressione ENTER para continuar...")
