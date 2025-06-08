import json
from utils.fila import Fila
from classes.pedido import Pedido

CAMINHO_PEDIDOS = "database/pedidos_fila.json"

def carregar_fila_pedidos():
    """Carrega a lista de pedidos do JSON e a reconstrói como uma Fila."""
    fila = Fila()
    try:
        with open(CAMINHO_PEDIDOS, "r", encoding="utf-8") as f:
            lista_pedidos_dict = json.load(f)

        for pedido_dict in lista_pedidos_dict:
            # Recria o objeto Pedido a partir do dicionário
            pedido = Pedido(
                nome_solicitante=pedido_dict['nome_solicitante'],
                id_pedido=pedido_dict['id_pedido']
            )
            pedido.data_solicitacao = pedido_dict['data_solicitacao']
            pedido.itens = pedido_dict['itens']
            fila.enfileirar(pedido)

    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existe ou está vazio, retorna uma fila vazia
        pass
    return fila

def salvar_fila_pedidos(fila):
    """Converte a Fila de Pedidos para uma lista de dicionários e salva em JSON."""
    lista_para_salvar = []
    for pedido in fila._elementos:
        lista_para_salvar.append(pedido.to_dict())

    try:
        with open(CAMINHO_PEDIDOS, "w", encoding="utf-8") as f:
            json.dump(lista_para_salvar, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao salvar a fila de pedidos: {e}")
        return False