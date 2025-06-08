from utils.manipulador_json import carregar_json, salvar_json
from utils.estoque_persistencia import carregar_estoque, salvar_estoque
from classes.engradado import Engradado
from classes.categorias import carregar_categorias, gerenciar_categorias
from interface.estoque import armazenar_engradado_no_estoque
from classes.estoque import Estoque
from classes.engradado import Engradado
from datetime import datetime
import os

# ------------------------------
# Funções auxiliares
# ------------------------------
#Função pra exibir um cabeçalho padrão
def exibir_cabecalho():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 50)
    print("|  S T O O K   -   G E R E N C I A D O R   V1.0  |".center(50))
    print("=" * 50)
#Função para formatar o peso para kg
def formatar_peso(peso_raw):
    try:
        peso_float = float(peso_raw.replace(",", "."))
        return f"{peso_float:.3f} kg"
    except:
        return "peso inválido"
#Função para solicitar data dentro do padrão br
def solicitar_data(campo):
    while True:
        data = input(f"{campo} (dd/mm/aaaa): ").strip()
        try:
            return datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            print(f"[!] {campo} inválida. Tente novamente.")
#Função para solicitar valor monetário no padrão R$
def solicitar_valor(campo):
    while True:
        valor = input(f"{campo} (ex: 9,99): ").strip().replace(",", ".")
        try:
            valor_float = round(float(valor), 2)
            valor_formatado = f"R$ {valor_float:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
            return valor_formatado
        except ValueError:
            print(f"[!] {campo} inválido. Tente novamente.")
# Espera confirmação do usuário
def pausar(mensagem="Pressione ENTER para continuar..."):
    input(f"\n{mensagem}")

# ------------------------------
# Menu principal e submenu
# ------------------------------
#Opções Menu Principal
def menu_principal():
    print("[ 1 ] Gerenciar Produtos")
    print("[ 2 ] Criar Engradado")
    print("[ 3 ] Armazenar Engradado")
    print("[ 0 ] Sair")
    return input("\nEscolha uma opção: ")
#Opções Submenu -> Produtos
def submenu_produtos():
    while True:
        exibir_cabecalho()
        print("|                GERENCIAR PRODUTOS               |")
        print("=" * 50)
        print("[ 1 ]  Cadastrar novo produto")
        print("[ 2 ] Listar todos os produtos")
        print("[ 3 ] Atualizar produto existente")
        print("[ 4 ] Remover produto")
        print("[ 5 ] Gerenciar categorias")
        print("[ 0 ] Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            listar_produtos()
        elif opcao == '3':
            atualizar_produto()
        elif opcao == '4':
            remover_produto()
        elif opcao == '5':
            gerenciar_categorias()
        elif opcao == '0':
            break
        else:
            print(f"\nOpção inválida. Tente novamente.")
        input(f"\nPressione ENTER para continuar...")

# ------------------------------
# Funções CRUD de Produto
# ------------------------------
# Função que Lista os Produtos Cadastrados
def listar_produtos():
    exibir_cabecalho()
    produtos = carregar_json("database/produtos.json")
    categorias = carregar_json("database/categorias.json")

    if not produtos:
        print("=" * 50)
        print("=== Lista de Produtos por Categoria ===\n")
        print("Nenhum produto cadastrado.") #Se não houver retorna esta mensagem
        return

    print("=" * 50) #Se houver dados cadastrados mostra os produtos por categoria
    print("=== Lista de Produtos por Categoria ===\n")
    agrupados = {}
    for codigo, info in produtos.items():
        cat = info.get("categoria", "Sem Categoria")
        agrupados.setdefault(cat, []).append((codigo, info))

    for cat, lista in agrupados.items():
        nome_categoria = categorias.get(cat, cat.title())
        print(f"\n📦 Categoria: {nome_categoria}")
        for codigo, info in lista:
            peso_formatado = formatar_peso(info["peso"])
            print(f"- {codigo} - {info['nome']} ({peso_formatado})")
# Função para cadastrar novo produto
def cadastrar_produto():
    exibir_cabecalho()
    caminho = "database/produtos.json"
    produtos = carregar_json(caminho)
    categorias = carregar_categorias()

    if not categorias:
        print("⚠️ Nenhuma categoria cadastrada. Cadastre primeiro.")
        input("\nPressione ENTER para voltar...")
        return

    print("|               Cadastro de Novo Produto                |")
    print("=" * 50)
    campos = {
        "codigo": "[vazio]",
        "nome": "[vazio]",
        "peso": "[vazio]",
        "fabricante": "[vazio]",
        "categoria": "[vazio]"
    }

    for campo in ["codigo", "nome", "peso", "fabricante"]:
        while True:
            exibir_cabecalho()
            print("Preenchimento dos dados:\n")
            for chave, valor in campos.items():
                print(f"{chave.capitalize()}: {valor}")
            entrada = input(f"\nInforme o valor para '{campo}': ").strip()
            if entrada:
                campos[campo] = entrada
                break
            else:
                print(f"[!] O campo '{campo}' não pode ficar vazio.")
                input("Pressione ENTER para tentar novamente...")

    # Escolha da categoria via enum-like
    chaves = list(categorias.keys())
    print("\nSelecione a categoria:")
    for i, chave in enumerate(chaves, 1):
        print(f"[{i}] {categorias[chave]}")

    while True:
        try:
            escolha = int(input("\nEscolha o número da categoria: "))
            if 1 <= escolha <= len(chaves):
                campos["categoria"] = chaves[escolha - 1]
                break
            else:
                print("Número fora do intervalo.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

    # Verificação de código duplicado
    if campos["codigo"] in produtos:
        print(f"\n[!] Já existe um produto com o código '{campos['codigo']}'.")
        return

    # Confirmação
    exibir_cabecalho()
    print("Resumo do produto a ser cadastrado:\n")
    for chave, valor in campos.items():
        print(f"{chave.capitalize()}: {valor}")

    while True:
        try:
            opcao = int(input("\nDeseja cadastrar o produto?\n[ 1 ] Sim     [ 2 ] Não\n> "))
            if opcao == 1:
                produtos[campos["codigo"]] = {
                    "nome": campos["nome"],
                    "peso": campos["peso"],
                    "fabricante": campos["fabricante"],
                    "categoria": campos["categoria"]
                }
                if salvar_json(produtos, caminho):
                    print("\n✅ Produto cadastrado com sucesso!")
                else:
                    print("\n❌ Erro ao salvar o produto.")
                input("\nPressione ENTER para voltar ao menu...")
                return
            elif opcao == 2:
                print("\n❌ Cadastro cancelado pelo usuário.")
                input("\nPressione ENTER para voltar ao menu...")
                return
            else:
                print("[!] Opção inválida. Digite 1 ou 2.")
        except ValueError:
            print("[!] Entrada inválida. Digite apenas 1 ou 2.")
# Função para atualizar produtos já cadastrados
def atualizar_produto():
    exibir_cabecalho()
    caminho = "database/produtos.json"
    produtos = carregar_json(caminho)

    if not produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    print("=== Produtos Cadastrados ===")
    for codigo, info in produtos.items():
        print(f"{codigo} - {info['nome']}")

    codigo = input("\nDigite o código do produto a atualizar: ").strip()
    if codigo not in produtos:
        print("[!] Produto não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")

    nome = input(f"Nome [{produtos[codigo]['nome']}]: ").strip()
    peso = input(f"Peso [{produtos[codigo]['peso']}]: ").strip()
    fabricante = input(f"Fabricante [{produtos[codigo]['fabricante']}]: ").strip()
    categoria = input(f"Categoria [{produtos[codigo]['categoria']}]: ").strip()

    if nome:
        produtos[codigo]['nome'] = nome
    if peso:
        produtos[codigo]['peso'] = peso
    if fabricante:
        produtos[codigo]['fabricante'] = fabricante
    if categoria:
        produtos[codigo]['categoria'] = categoria

    while True:
        try:
            confirmacao = int(input("\nDeseja salvar as alterações?\n[ 1 ] Sim     [ 2 ] Não\n> "))
            if confirmacao == 1:
                if salvar_json(produtos, caminho):
                    print("\n✅ Produto atualizado com sucesso!")
                else:
                    print("\n❌ Erro ao salvar o produto.")
                break
            elif confirmacao == 2:
                print("\n❌ Alterações canceladas.")
                break
            else:
                print("[!] Opção inválida. Digite 1 ou 2.")
        except ValueError:
            print("[!] Entrada inválida. Digite apenas 1 ou 2.")

# Função para remover produtos cadastrados
def remover_produto():
    exibir_cabecalho()
    caminho = "database/produtos.json"
    produtos = carregar_json(caminho)

    if not produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    print("=== Produtos Cadastrados ===")
    for codigo, info in produtos.items():
        print(f"{codigo} - {info['nome']}")

    codigo = input("\nDigite o código do produto a remover: ").strip()
    if codigo not in produtos:
        print("[!] Produto não encontrado.")
        return

    print("\nInformações do produto selecionado:")
    for chave, valor in produtos[codigo].items():
        print(f"{chave.capitalize()}: {valor}")

    while True:
        try:
            confirmacao = int(input("\nDeseja realmente remover este produto?\n[ 1 ] Sim     [ 2 ] Não\n> "))
            if confirmacao == 1:
                del produtos[codigo]
                if salvar_json(produtos, caminho):
                    print("\n✅ Produto removido com sucesso.")
                else:
                    print("\n❌ Erro ao salvar após remoção.")
                break
            elif confirmacao == 2:
                print("\n❌ Remoção cancelada.")
                break
            else:
                print("[!] Opção inválida. Digite 1 ou 2.")
        except ValueError:
            print("[!] Entrada inválida. Digite apenas 1 ou 2.")

    # (Mesma estrutura com listagem, input e confirmação de exclusão)
    pass

# ------------------------------
# Função de criação de Engradado
# ------------------------------
#Cria um Engradado ou pallet para armazenar 
def criar_engradado():
    exibir_cabecalho()
    produtos = carregar_json("database/produtos.json")

    if not produtos:
        print("⚠️ Nenhum produto cadastrado.")
        return

    print("=== Criar Engradado ===")
    print("\nProdutos disponíveis:")
    for codigo, info in produtos.items():
        peso_formatado = formatar_peso(info["peso"])
        print(f"-> {codigo}: {info['nome']} ({peso_formatado})")

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
    validade = solicitar_data("Data de validade")
    fabricacao = solicitar_data("Data de fabricação")
    preco_compra = solicitar_valor("Preço de compra")
    preco_venda = solicitar_valor("Preço de venda")
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
    caminho = "database/engradados.json"
    engradados = carregar_json(caminho)

    novo_id = f"ENG{str(len(engradados) + 1).zfill(3)}"

    engradados[novo_id] = {
        "codigo_produto": codigo,
        "quantidade": quantidade,
        "lote": lote,
        "validade": validade,
        "fabricacao": fabricacao,
        "preco_compra": preco_compra,
        "preco_venda": preco_venda,
        "fornecedor": fornecedor
    }

    if salvar_json(engradados, caminho):
        print(f"📦 Engradado salvo com o ID: {novo_id}")
    else:
        print("❌ Erro ao salvar o engradado.")



#Armazena o engradado em algum espaço possivel
def menu_armazenar_engradado():
    exibir_cabecalho()
    print("ARMAZENAR ENGRADADO NO ESTOQUE".center(50, " "))
    print("=" * 50)

    # Carrega os engradados disponíveis que ainda não foram para o estoque
    caminho_engradados = "database/engradados.json"
    engradados_dict = carregar_json(caminho_engradados)
    if not engradados_dict:
        print("⚠️ Nenhum engradado disponível para armazenar.")
        pausar()
        return

    # Exibe os engradados disponíveis para seleção
    print(f"\nEngradados disponíveis:\n")
    ids_engradados = list(engradados_dict.keys())
    for idx, eng_id in enumerate(ids_engradados, 1):
        eng = engradados_dict[eng_id]
        print(f"[{idx}] ID: {eng_id} | Produto: {eng['codigo_produto']} | Lote: {eng['lote']}")

    # Seleção do engradado pelo usuário
    try:
        escolha = int(input(f"\nEscolha o número do engradado: "))
        if not (1 <= escolha <= len(ids_engradados)):
            raise ValueError("Número fora do intervalo.")
    except ValueError:
        print("[!] Entrada inválida.")
        pausar()
        return

    id_selecionado = ids_engradados[escolha - 1]
    dados_engradado = engradados_dict[id_selecionado]
    engradado_obj = Engradado(**dados_engradado)

    # Carrega o estado atual do estoque usando a função correta
    estoque = carregar_estoque()

    # Mostra as posições válidas para o engradado selecionado
    print("\nEndereços disponíveis para este produto:")
    posicoes_validas = []
    for posicao, pilha in estoque.galpao.items():
        topo = pilha.topo()
        # Condições: a pilha não está cheia E (está vazia OU o produto no topo é o mesmo)
        if len(pilha.pilha) < 5 and (pilha.esta_vazia() or topo.codigo_produto == engradado_obj.codigo_produto):
            produto_topo = f"Produto: {topo.codigo_produto}" if topo else "Vazio"
            print(f"  - {posicao} (Ocupado: {len(pilha.pilha)}/5) | {produto_topo}")
            posicoes_validas.append(posicao)
    
    if not posicoes_validas:
        print("\n[!] Não há nenhuma posição disponível para este tipo de produto no momento.")
        pausar()
        return

    # Solicita o destino e armazena
    destino = input("\nDigite o endereço onde deseja armazenar (ex: B3): ").strip().upper()
    if destino not in posicoes_validas:
        print("[!] Endereço inválido ou não disponível para este produto.")
        pausar()
        return

    # Armazena o engradado na posição e salva o estado do estoque
    if estoque.armazenar_engradado(destino, engradado_obj):
        print(f"\n✅ Engradado {id_selecionado} armazenado com sucesso em {destino}.")
        
        # Remove o engradado da lista de "disponíveis" e salva a alteração
        del engradados_dict[id_selecionado]
        salvar_json(engradados_dict, caminho_engradados)
        
        # Salva o estado atualizado do estoque usando a função correta
        salvar_estoque(estoque)
    else:
        # Esta mensagem apareceria se a pilha estivesse cheia, mas a lógica já previne isso
        print("❌ Falha ao armazenar o engradado.")

    pausar()