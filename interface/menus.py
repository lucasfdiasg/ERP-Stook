from utils.manipulador_json import carregar_json, salvar_json
from utils.estoque_persistencia import carregar_estoque, salvar_estoque
from utils.pedidos_persistencia import carregar_fila_pedidos, salvar_fila_pedidos, registrar_pedido_processado
from classes.engradado import Engradado
from classes.categorias import carregar_categorias, gerenciar_categorias
from classes.estoque import Estoque
from utils.exibicao import exibir_cabecalho, pausar
from classes.pedido import Pedido
from datetime import datetime
from utils.exibicao import exibir_cabecalho, pausar, limpar_tela
from datetime import datetime, timedelta
from utils.estoque_persistencia import carregar_estoque
import os

# ------------------------------
# Funções auxiliares
# ------------------------------
#Funçao para limpar terminal
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
            print(f"🚨 {campo} inválida. Tente novamente.")
#Função para solicitar valor monetário no padrão R$
def solicitar_valor(campo):
    while True:
        valor = input(f"{campo} (ex: 9,99): ").strip().replace(",", ".")
        try:
            valor_float = round(float(valor), 2)
            valor_formatado = f"R$ {valor_float:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
            return valor_formatado
        except ValueError:
            print(f"🚨 {campo} inválido. Tente novamente.")


# ------------------------------
# Menu principal e submenu
# ------------------------------
#Opções Menu Principal
def menu_principal():
    print("[ 1 ] Gerenciar Produtos")
    print("[ 2 ] Criar Engradado")
    print("[ 3 ] Armazenar Engradado")
    print("[ 4 ] Gerenciar Pedidos")  # Agora aponta para o submenu
    print("[ 5 ] Visualizar Histórico de Pedidos")
    print("[ 6 ] Visualizar Estoque")
    print("[ 7 ] Remover Engradado do Estoque")
    print("[ 8 ] Relatórios")
    print("[ 0 ] Sair")
    return input("\nEscolha uma opção acima\n\n>>> ")
#Opções Submenu -> Produtos
def submenu_produtos():
    while True:
        exibir_cabecalho()
        print("|                GERENCIAR PRODUTOS              |")
        print("=" * 50)
        print("[ 1 ] Cadastrar novo produto")
        print("[ 2 ] Listar todos os produtos")
        print("[ 3 ] Atualizar produto existente")
        print("[ 4 ] Remover produto")
        print("[ 5 ] Gerenciar categorias")
        print("[ 0 ] Voltar ao menu principal")

        opcao = input("\nEscolha uma opção acima\n\n>>> ")

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
            input(f"\nPressione ENTER\n\n>>>")
#Opções Submenu -> Pedidos
def submenu_pedidos():
    while True:
        exibir_cabecalho()
        print("|                 GERENCIAR PEDIDOS                 |")
        print("=" * 50)
        print("[ 1 ] Registrar Novo Pedido")
        print("[ 2 ] Processar Próximo Pedido")
        print("[ 3 ] Visualizar Fila de Pedidos")
        print("[ 0 ] Voltar ao menu principal")

        opcao = input("\nEscolha uma opção acima\n\n>>> ")

        if opcao == '1':
            registrar_novo_pedido()
        elif opcao == '2':
            processar_pedido()
        elif opcao == '3':
            visualizar_fila_pedidos()

        elif opcao == '0':
            break
        else:
            print(f"\nOpção inválida. Tente novamente.")
            input(f"\nPressione ENTER\n\n>>>")
#Opções Submenu -> Relatório
def menu_relatorios():
    while True:
        exibir_cabecalho()
        print("|                 MENU DE RELATÓRIOS                |")
        print("=" * 50)
        print("[ 1 ] Produtos próximos do vencimento (30 dias)")
        print("[ 0 ] Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            exibir_produtos_vencendo()
        elif opcao == '0':
            break
        else:
            print(f"\nOpção inválida. Tente novamente.")
            input(f"\nPressione ENTER\n\n>>>")


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
    input(f"\nPressione ENTER para RETORNAR\n\n>>>")
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
            print("|            Cadastro de Novo Produto            |")
            print("=" * 50)
            for chave, valor in campos.items():
                print(f"{chave.capitalize()}: {valor}")
            entrada = input(f"\nInforme o valor para '{campo}': ").strip()
            if entrada:
                campos[campo] = entrada
                break
            else:
                print(f"🚨 O campo '{campo}' não pode ficar vazio.")
                (f"\nPressione ENTER\n\n>>>")

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
                if salvar_json(caminho, produtos):
                    print("\n✅ Produto cadastrado com sucesso!")
                else:
                    print("\n❌ Erro ao salvar o produto.")
                input(f"\nPressione ENTER para RETORNAR\n\n>>>")
                return
            elif opcao == 2:
                print("\n❌ Cadastro cancelado pelo usuário.")
                input(f"\nPressione ENTER para RETORNAR\n\n>>>")
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

    print(f"=== Produtos Cadastrados ===\n")
    for codigo, info in produtos.items():
        print(f"{codigo} - {info['nome']}")

    codigo = input(f"\nDigite o código do produto a atualizar\
                   \nOu ENTER para RETORNAR\n\n>>>").strip()
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

    codigo = input(F"\nDigite o código do produto a remover\
                   \nou ENTER para RETORNAR\n\n>>>").strip()
    if codigo not in produtos:
        print("🚨 Produto não encontrado.")
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
                print("🚨 Opção inválida. Digite 1 ou 2.")
        except ValueError:
            print("🚨 Entrada inválida. Digite apenas 1 ou 2.")

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
        print("🚨 Produto não encontrado.")
        return

    try:
        quantidade = int(input("Quantidade de itens: "))
        if quantidade <= 0:
            raise ValueError
    except ValueError:
        print("🚨 Quantidade inválida.")
        return

    lote = input("Lote: ").strip()
    validade = solicitar_data("Data de validade")
    fabricacao = solicitar_data("Data de fabricação")
    preco_compra = solicitar_valor("Preço de compra")
    preco_venda = solicitar_valor("Preço de venda")
    fornecedor = input("Fornecedor: ").strip()

    engradado_obj = Engradado(
        codigo_produto=codigo,
        quantidade=quantidade,
        lote=lote,
        validade=validade,
        fabricacao=fabricacao,
        preco_compra=preco_compra,
        preco_venda=preco_venda,
        fornecedor=fornecedor
    )

    print(f"\n✅ Engradado criado com sucesso:\n{engradado_obj}")
    caminho = "database/engradados.json"
    engradados = carregar_json(caminho)

    novo_id = f"ENG{str(len(engradados) + 1).zfill(3)}"

    engradados[novo_id] = engradado_obj.to_dict()

    if salvar_json(caminho, engradados):
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
    produtos = carregar_json("database/produtos.json")  # carrega nomes dos produtos

    for idx, eng_id in enumerate(ids_engradados, 1):
        eng = engradados_dict[eng_id]
        codigo = eng['codigo_produto']
        nome = produtos.get(codigo, {}).get("nome", "Desconhecido")
        print(f"[{idx}] {nome} | Produto: {codigo} | Lote: {eng['lote']}")


    # Seleção do engradado pelo usuário
    try:
        escolha = int(input(f"\nEscolha o número do engradado: "))
        if not (1 <= escolha <= len(ids_engradados)):
            raise ValueError("Número fora do intervalo.")
    except ValueError:
        print("🚨 Entrada inválida.")
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
        print("\n🚨 Não há nenhuma posição disponível para este tipo de produto no momento.")
        pausar()
        return

    # Solicita o destino e armazena
    destino = input("\nDigite o endereço onde deseja armazenar (ex: B3): ").strip().upper()
    if destino not in posicoes_validas:
        print("🚨 Endereço inválido ou não disponível para este produto.")
        pausar()
        return

    # Armazena o engradado na posição e salva o estado do estoque
    if estoque.armazenar_engradado(destino, engradado_obj):
        print(f"\n✅ Engradado {id_selecionado} armazenado com sucesso em {destino}.")
        
        # Remove o engradado da lista de "disponíveis" e salva a alteração
        del engradados_dict[id_selecionado]
        salvar_json(caminho_engradados, engradados_dict) # Argumentos na ordem correta
        
        # Salva o estado atualizado do estoque usando a função correta
        salvar_estoque(estoque)
    else:
        # Esta mensagem apareceria se a pilha estivesse cheia, mas a lógica já previne isso
        print("❌ Falha ao armazenar o engradado.")

    pausar()

# Função para exibir o conteúdo do estoque
def visualizar_estoque_detalhado():
    exibir_cabecalho()  # Mantém o cabeçalho padrão de 50 caracteres

    estoque = carregar_estoque()
    produtos = carregar_json("database/produtos.json")

    # --- Função auxiliar interna para formatar cada célula do grid ---
    def formatar_celula(posicao, pilha_obj, largura):
        if not pilha_obj:
            return " " * largura

        info_formatada = f"{posicao}:Vazio"
        if not pilha_obj.esta_vazia():
            ocupacao = len(pilha_obj.pilha)
            barra = "▉" * ocupacao + "░" * (5 - ocupacao)
            cod_produto = pilha_obj.topo().codigo_produto
            info_formatada = f"{posicao}:[{barra}] {cod_produto}"
        
        return info_formatada.ljust(largura)

    # --- Bloco 1: Colunas A e B (Laterais) ---
    for linha in range(1, 9):
        # A e B agora têm 16 de largura para alinhar com C, D, E
        celula_a = formatar_celula(f"A{linha}", estoque.galpao.get(f"A{linha}"), 16)
        celula_b = formatar_celula(f"B{linha}", estoque.galpao.get(f"B{linha}"), 16)
        
        # O espaço central foi calculado para alinhar B com E (18 espaços)
        print(f"{celula_a}{' ' * 18}{celula_b}")

    # --- Corredor Principal ---
    print("=" * 50)
    print("||".center(50))
    print("=" * 50)

    # --- Bloco 2: Colunas C, D e E (Central) ---
    for linha in range(1, 9):
        celula_c = formatar_celula(f"C{linha}", estoque.galpao.get(f"C{linha}"), 16)
        celula_d = formatar_celula(f"D{linha}", estoque.galpao.get(f"D{linha}"), 16)
        celula_e = formatar_celula(f"E{linha}", estoque.galpao.get(f"E{linha}"), 16)
        
        print(f"{celula_c}{celula_d}{celula_e}")
    
    print("-" * 50)

    # --- Legenda (Formatada para o limite de 50 caracteres) ---
    print("\nLEGENDA DE PRODUTOS NO ESTOQUE:")
    produtos_em_estoque = {}
    for pos, pilha in estoque.galpao.items():
        if not pilha.esta_vazia():
            topo = pilha.topo()
            if topo.codigo_produto not in produtos_em_estoque:
                nome = produtos.get(topo.codigo_produto, {}).get("nome", "Desconhecido")
                produtos_em_estoque[topo.codigo_produto] = nome
    
    if not produtos_em_estoque:
        print("Nenhum produto encontrado no estoque.")
    else:
        for codigo, nome in produtos_em_estoque.items():
            legenda_item = f"- {codigo}: {nome}"
            print(legenda_item[:50])

    pausar()

# ------------------------------
# Função de criação pedidos
# ------------------------------
#Função que adiciona novos pedidos à fila de pedidos
def registrar_novo_pedido():
    exibir_cabecalho()
    print("|       REGISTRO DE NOVO PEDIDO (ATACADO)        |")
    print("=" * 50)

    produtos = carregar_json("database/produtos.json")
    estoque = carregar_estoque()

    if not produtos:
        print("Nenhum produto cadastrado no sistema.")
        return pausar()

    nome_solicitante = input("Nome do solicitante: ").strip()
    if not nome_solicitante:
        print("🚨 O nome do solicitante é obrigatório.")
        return pausar()

    # Identificar os produtos com engradados disponíveis no estoque
    produtos_disponiveis = {}
    for posicao, pilha in estoque.galpao.items():
        if not pilha.esta_vazia():
            topo = pilha.topo()
            codigo = topo.codigo_produto
            produtos_disponiveis[codigo] = produtos.get(codigo, {"nome": "Desconhecido"})

    if not produtos_disponiveis:
        print("❌ Nenhum produto disponível no estoque para pedidos.")
        return pausar()

    fila_pedidos = carregar_fila_pedidos()
    novo_id = f"PED{len(fila_pedidos) + 1:03d}"
    novo_pedido = Pedido(nome_solicitante, novo_id)

    while True:
        print("\n--- Adicionar Engradado ao Pedido ---")
        for codigo, info in produtos_disponiveis.items():
            print(f"- {codigo}: {info['nome']}")

        codigo_produto = input("Digite o código do produto (ou '0' para finalizar): ").strip()
        if codigo_produto == '0':
            break

        if codigo_produto not in produtos_disponiveis:
            print("🚨 Produto não disponível no estoque.")
            continue

        try:
            quantidade = int(input("Quantidade de ENGRADADOS: ").strip())
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            print("🚨 Quantidade inválida.")
            continue

        if novo_pedido.adicionar_item(codigo_produto, quantidade):
            print("✅ Engradado(s) adicionado(s) ao pedido.")

        input("\nPressione ENTER para continuar adicionando ou finalizar...")

    if not novo_pedido.itens:
        print("\nNenhum item adicionado. Pedido cancelado.")
    else:
        fila_pedidos.enfileirar(novo_pedido)
        if salvar_fila_pedidos(fila_pedidos):
            print(f"\n✅ Pedido {novo_id} registrado com sucesso!")
        else:
            print("\n🚨 Erro ao salvar o pedido.")

    pausar()

#Função que remove um engradado do estoque
def remover_engradado_do_estoque():
    """
    Remove o engradado do topo de uma pilha selecionada no estoque.
    """
    # Reutilizamos a função de visualização para o usuário ver o que pode remover
    visualizar_estoque_detalhado()

    # Carrega o estado atual para manipulação
    estoque = carregar_estoque()

    posicao = input("\nDigite a posição do engradado a ser removido (ex: A1): ").strip().upper()

    # Validação 1: A posição existe no galpão?
    if posicao not in estoque.galpao:
        print("\n🚨 Posição inválida.")
        pausar()
        return

    # Validação 2: A pilha na posição não está vazia?
    if estoque.galpao[posicao].esta_vazia():
        print(f"\n🚨 Não há engradados na posição {posicao}.")
        pausar()
        return

    # Se as validações passaram, remove o engradado
    engradado_removido = estoque.remover_engradado(posicao)

    if engradado_removido:
        # Salva o novo estado do estoque no arquivo JSON
        if salvar_estoque(estoque):
            print(f"\n✅ Engradado removido com sucesso da posição {posicao}.")
            print(f"   Produto: {engradado_removido.codigo_produto} | Lote: {engradado_removido.lote}")
        else:
            print("\n🚨 Erro ao salvar o estado do estoque após a remoção.")
    else:
        print("\n🚨 Falha ao remover o engradado.")

    pausar()
# Função que processa os pedidos
def processar_pedido():
    exibir_cabecalho()
    print("PROCESSAR PRÓXIMO PEDIDO".center(50))
    print("=" * 50)

    fila = carregar_fila_pedidos()
    if fila.esta_vazia():
        print("📭 Nenhum pedido na fila.")
        return pausar()

    pedido = fila.desenfileirar()
    print(f"🧾 Pedido ID: {pedido.id_pedido} | Solicitante: {pedido.nome_solicitante}")
    print("-" * 50)

    estoque = carregar_estoque()

    # -----------------------
    # FASE 1: VERIFICAÇÃO
    # -----------------------
    estoque_temporario = {pos: list(pilha.pilha) for pos, pilha in estoque.galpao.items()}
    pode_atender = True
    faltantes = {}

    for item in pedido.itens:
        codigo = item["codigo_produto"]
        quantidade = int(item["quantidade"])
        retirados = 0

        for posicao, pilha_copia in estoque_temporario.items():
            if pilha_copia and pilha_copia[-1].codigo_produto == codigo:
                while pilha_copia and pilha_copia[-1].codigo_produto == codigo and retirados < quantidade:
                    pilha_copia.pop()
                    retirados += 1
            if retirados == quantidade:
                break

        if retirados < quantidade:
            pode_atender = False
            faltantes[codigo] = quantidade - retirados

    # -----------------------
    # FASE 2: EXECUÇÃO
    # -----------------------
    if not pode_atender:
        print("⚠️ Pedido não pôde ser atendido totalmente.")
        for cod, faltam in faltantes.items():
            print(f"❌ Faltaram {faltam} engradado(s) de {cod} no estoque.")
        
        # Devolve o pedido para o início da fila se não puder ser atendido
        # (Opcional, mas boa prática. Se preferir descartar, remova as 3 linhas abaixo)
        fila_nova = Fila()
        fila_nova.enfileirar(pedido)
        for p in fila._elementos:
            fila_nova.enfileirar(p)
        
        salvar_fila_pedidos(fila_nova)
        # O pedido NÃO é registrado no histórico, pois não foi processado
        return pausar()

    # Se passou na verificação, agora de fato altera o estoque real
    for item in pedido.itens:
        codigo = item["codigo_produto"]
        quantidade = int(item["quantidade"])
        restantes = quantidade

        for posicao, pilha in estoque.galpao.items():
            while not pilha.esta_vazia() and pilha.topo().codigo_produto == codigo and restantes > 0:
                pilha.desempilhar()
                restantes -= 1
                print(f"✅ Retirado 1 engradado de {codigo} da posição {posicao}.")

            if restantes == 0:
                break

    salvar_estoque(estoque)
    salvar_fila_pedidos(fila) # Salva a fila sem o pedido que foi processado
    registrar_pedido_processado(pedido, completo=True)
    print("\n🎉 Pedido atendido COMPLETAMENTE!")
    pausar()
    exibir_cabecalho()
    print("PROCESSAR PRÓXIMO PEDIDO".center(50))
    print("=" * 50)

    fila = carregar_fila_pedidos()
    if fila.esta_vazia():
        print("📭 Nenhum pedido na fila.")
        return pausar()

    pedido = fila.desenfileirar()
    print(f"🧾 Pedido ID: {pedido.id_pedido} | Solicitante: {pedido.nome_solicitante}")
    print("-" * 50)

    estoque = carregar_estoque()

    # -----------------------
    # FASE 1: VERIFICAÇÃO
    # -----------------------
    estoque_temporario = {pos: list(pilha.pilha) for pos, pilha in estoque.galpao.items()}
    pode_atender = True
    faltantes = {}

    for item in pedido.itens:
        codigo = item["codigo_produto"]
        quantidade = int(item["quantidade"])
        retirados = 0

        for posicao, pilha_copia in estoque_temporario.items():
            if pilha_copia and pilha_copia[-1].codigo_produto == codigo:
                while pilha_copia and pilha_copia[-1].codigo_produto == codigo and retirados < quantidade:
                    pilha_copia.pop()
                    retirados += 1

            if retirados == quantidade:
                break

        if retirados < quantidade:
            pode_atender = False
            faltantes[codigo] = quantidade - retirados

    # -----------------------
    # FASE 2: EXECUÇÃO
    # -----------------------
    if not pode_atender:
        print("⚠️ Pedido não pôde ser atendido totalmente.")
        for cod, faltam in faltantes.items():
            print(f"❌ Faltaram {faltam} engradado(s) de {cod} no estoque.")
        registrar_pedido_processado(pedido, completo=False)
        salvar_fila_pedidos(fila)  # Atualiza a fila com o pedido removido
        return pausar()

    # Se passou na verificação, agora de fato altera o estoque real
    for item in pedido.itens:
        codigo = item["codigo_produto"]
        quantidade = int(item["quantidade"])
        restantes = quantidade

        for posicao, pilha in estoque.galpao.items():
            while not pilha.esta_vazia() and pilha.topo().codigo_produto == codigo and restantes > 0:
                pilha.desempilhar()
                restantes -= 1
                print(f"✅ Retirado 1 engradado de {codigo} da posição {posicao}.")

            if restantes == 0:
                break

    salvar_estoque(estoque)
    salvar_fila_pedidos(fila)
    registrar_pedido_processado(pedido, completo=True)
    print("\n🎉 Pedido atendido COMPLETAMENTE!")
    pausar()


    # Atualiza estoque e fila
    salvar_estoque(estoque)
    salvar_fila_pedidos(fila)

    if atendido_completo:
        print("\n🎉 Pedido atendido COMPLETAMENTE!")
    else:
        print("\n⚠️ Pedido atendido PARCIALMENTE.")

    registrar_pedido_processado(pedido, completo=atendido_completo)
    pausar()
    
#Função que exibe o histórico de pedidos
def visualizar_historico_pedidos():
    exibir_cabecalho()
    print("HISTÓRICO DE PEDIDOS ATENDIDOS".center(50))
    print("=" * 50)

    historico = carregar_json("database/historico_pedidos.json")
    if not historico:
        print("📭 Nenhum pedido processado ainda.")
        return pausar()

    for pedido_id, dados in historico.items():
        print(f"\n🧾 Pedido ID: {pedido_id}")
        print(f"👤 Solicitante: {dados['solicitante']}")
        print(f"📦 Status: {'✅ Completo' if dados['status'] == 'Completo' else '⚠️ Parcial'}")
        print("Engradados pedidos:")
        for item in dados["itens"]:
            cod = item["codigo_produto"]
            qtd = item["quantidade"]
            print(f" - {cod}: {qtd} engradado(s)")
        print("-" * 50)

    pausar()

#Função que mostra a fila de pedidos
def visualizar_fila_pedidos():
    exibir_cabecalho()
    print("FILA DE PEDIDOS PENDENTES".center(50))
    print("=" * 50)

    fila = carregar_fila_pedidos()
    if fila.esta_vazia():
        print("📭 Nenhum pedido na fila.")
        return pausar()

    for idx, pedido in enumerate(fila._elementos, 1):
        print(f"\n[{idx}] Pedido ID: {pedido.id_pedido}")
        print(f"👤 Solicitante: {pedido.nome_solicitante}")
        print(f"📅 Data: {pedido.data_solicitacao}")
        print("Itens:")
        for item in pedido.itens:
            print(f" - {item['codigo_produto']}: {item['quantidade']} un.")
        print("-" * 50)

    pausar()


# ------------------------------
# Função de criação relatórios
# ------------------------------
# Função que varre o estoque e coleta engradados
def exibir_produtos_vencendo():
    exibir_cabecalho()
    print("RELATÓRIO: PRODUTOS PRÓXIMOS DO VENCIMENTO".center(50))
    print("=" * 50)

    estoque = carregar_estoque()
    lista_engradados = []

    for pilha in estoque.galpao.values():
        lista_engradados.extend(pilha.pilha)

    if not lista_engradados:
        print("📦 Nenhum engradado armazenado no estoque.")
    else:
        print("Engradados vencendo em até 30 dias:\n")
        verificar_validade_recursiva(lista_engradados, estoque.galpao)


    pausar()
# Função Recursiva
def verificar_validade_recursiva(lista, posicoes=None):
    if not lista:
        return

    engradado = lista[0]
    restante = lista[1:]

    try:
        validade = datetime.strptime(engradado.validade, "%d/%m/%Y")
        hoje = datetime.now()
        dias_para_vencer = (validade - hoje).days

        if 0 <= dias_para_vencer <= 30:
            # Descobre onde está estocado
            posicao = "Desconhecida"
            if posicoes:
                for pos, pilha in posicoes.items():
                    if engradado in pilha.pilha:
                        posicao = pos
                        break

            print(f"⚠️ Produto: {engradado.codigo_produto}")
            print(f"   Lote: {engradado.lote}")
            print(f"   Validade: {engradado.validade} ({dias_para_vencer} dia(s))")
            print(f"   Localização: {posicao}")
            print("-" * 50)
    except Exception as e:
        print(f"[ERRO] Validade inválida para engradado: {e}")

    verificar_validade_recursiva(restante, posicoes)



