from utils.manipulador_json import carregar_json, salvar_json
from classes.engradado import Engradado
from datetime import datetime
import os


# Cabeçalho do sistema com limpeza de tela
def exibir_cabecalho():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 50)
    print("|  S T O O K   -   G E R E N C I A D O R   V1.0  |".center(50))
    print("=" * 50)

# Menu principal
def menu_principal():
    print("1. Cadastrar novo produto")
    print("2. Criar engradado")
    print("0. Sair")
    return input("\nEscolha uma opção: ")


# Função de validação de data no padrão brasileiro
def solicitar_data(campo):
    while True:
        data = input(f"{campo} (dd/mm/aaaa): ").strip()
        try:
            return datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            print(f"[!] {campo} inválida. Tente novamente.")

# Função para solicitar um valor monetário (com vírgula ou ponto)
def solicitar_valor(campo):
    while True:
        valor = input(f"{campo} (ex: 9,99): ").strip().replace(",", ".")
        try:
            return round(float(valor), 2)
        except ValueError:
            print(f"[!] {campo} inválido. Tente novamente.")

# Função principal de cadastro de produto
def cadastrar_produto():
    exibir_cabecalho()
    caminho = "database/produtos.json"
    produtos = carregar_json(caminho)

    print("=== Cadastro de Novo Produto ===")

    while True:
        codigo = input("Código do produto: ").strip()
        if codigo in produtos:
            print("[!] Código já cadastrado. Tente outro.")
        elif codigo == "":
            print("[!] Código não pode ser vazio.")
        else:
            break

    nome = input("Nome: ").strip()
    peso = input("Peso (kg): ").strip()
    fabricante = input("Fabricante: ").strip()
    categoria = input("Categoria: ").strip()

    produtos[codigo] = {
        "nome": nome,
        "peso": peso,
        "fabricante": fabricante,
        "categoria": categoria
    }

    if salvar_json(produtos, caminho):
        print("\n✅ Produto cadastrado com sucesso!")
    else:
        print("\n❌ Erro ao salvar o produto.")

# Função para criar um engradado com um único tipo de produto
def criar_engradado():
    exibir_cabecalho()
    caminho = "database/produtos.json"
    produtos = carregar_json(caminho)

    if not produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    print("=== Criar Engradado ===")
    print("\nProdutos disponíveis:")
    for codigo, info in produtos.items():
        print(f"-> {codigo}: {info['nome']}")

    codigo = input("\nCódigo do produto: ").strip()
    if codigo not in produtos:
        print("[!] Produto não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade de itens: "))
        if quantidade <= 0:
            raise ValueError
    except ValueError:
        print("[!] Quantidade inválida.")
        return

    lote = input("Lote: ").strip()
    validade = input("Data de validade (dd/mm/aaaa): ").strip()
    fabricacao = input("Data de fabricação (dd/mm/aaaa): ").strip()
    try:
        preco_compra = float(input("Preço de compra: ").replace(",", "."))
        preco_venda = float(input("Preço de venda: ").replace(",", "."))
    except ValueError:
        print("[!] Preço inválido.")
        return

    fornecedor = input("Fornecedor: ").strip()

    engradado = Engradado(
        codigo_produto=codigo,
        quantidade=quantidade,
        lote=lote,
        validade=validade,
        fabricacao=fabricacao,
        preco_compra=preco_compra,
        preco_venda=preco_venda,
        fornecedor=fornecedor
    )

    print(f"\n✅ Engradado criado com sucesso:\n{engradado}")
