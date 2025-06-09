import json
from utils.fila import Fila
from classes.pedido import Pedido
from utils.manipulador_json import carregar_json, salvar_json

# Caminho padrão do arquivo onde a fila de pedidos é armazenada
CAMINHO_PEDIDOS = "database/pedidos_fila.json"

# =======================================================
# Função para carregar os pedidos da fila
# -------------------------------------------------------
# Retorna:
# - Uma instância de Fila com objetos Pedido reconstruídos a partir do JSON
# =======================================================
def carregar_fila_pedidos():
    """Carrega a lista de pedidos do JSON e a reconstrói como uma Fila."""
    fila = Fila()

    try:
        # Abre o arquivo e carrega os pedidos salvos (lista de dicionários)
        with open(CAMINHO_PEDIDOS, "r", encoding="utf-8") as f:
            lista_pedidos_dict = json.load(f)

        # Para cada dicionário, cria um objeto Pedido e adiciona na fila
        for pedido_dict in lista_pedidos_dict:
            pedido = Pedido(
                nome_solicitante=pedido_dict['nome_solicitante'],
                id_pedido=pedido_dict['id_pedido']
            )
            pedido.data_solicitacao = pedido_dict['data_solicitacao']
            pedido.itens = pedido_dict['itens']
            fila.enfileirar(pedido)

    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existe ou está vazio/corrompido, retorna fila vazia
        pass

    return fila

# =======================================================
# Função para salvar a fila de pedidos no arquivo JSON
# -------------------------------------------------------
# Parâmetro:
# - fila: instância da classe Fila contendo objetos Pedido
# Retorna:
# - True se salvou com sucesso, False se houve erro
# =======================================================
def salvar_fila_pedidos(fila):
    """Converte a Fila de Pedidos para uma lista de dicionários e salva em JSON."""
    lista_para_salvar = []

    # Converte cada pedido em dicionário (usando to_dict())
    for pedido in fila._elementos:
        lista_para_salvar.append(pedido.to_dict())

    try:
        # Salva a lista como JSON no arquivo de pedidos
        with open(CAMINHO_PEDIDOS, "w", encoding="utf-8") as f:
            json.dump(lista_para_salvar, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao salvar a fila de pedidos: {e}")
        return False

# =======================================================
# Função para registrar um pedido processado no histórico
# -------------------------------------------------------
# Parâmetros:
# - pedido: instância da classe Pedido
# - completo: booleano indicando se foi totalmente atendido
# A informação vai para: database/historico_pedidos.json
# =======================================================
def registrar_pedido_processado(pedido, completo=True):
    caminho = "database/historico_pedidos.json"

    # Carrega o histórico existente (ou cria um novo dicionário vazio)
    historico = carregar_json(caminho) or {}

    # Adiciona o pedido processado ao histórico
    historico[pedido.id_pedido] = {
        "solicitante": pedido.nome_solicitante,
        "itens": pedido.itens,
        "status": "Completo" if completo else "Parcial"
    }

    # Salva o histórico atualizado no arquivo
    if not salvar_json(caminho, historico): 
        print("[ERRO] Não foi possível salvar o histórico de pedidos.")
