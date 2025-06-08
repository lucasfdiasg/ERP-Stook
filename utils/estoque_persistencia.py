import json
from classes.estoque import Estoque
from classes.engradado import Engradado
from classes.espaco_armazenamento import EspacoArmazenamento

CAMINHO_ESTOQUE = "database/estoque.json"

def salvar_estoque(estoque: Estoque):
    dados = {}
    for posicao, pilha in estoque.galpao.items():
        dados[posicao] = [eng.__dict__ for eng in pilha.pilha]
    try:
        with open(CAMINHO_ESTOQUE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao salvar estoque: {e}")
        return False

def carregar_estoque():
    estoque = Estoque()
    try:
        with open(CAMINHO_ESTOQUE, "r", encoding="utf-8") as f:
            dados = json.load(f)
        for posicao, lista_engradados in dados.items():
            for eng_dict in lista_engradados:
                eng = Engradado(**eng_dict)
                estoque.galpao[posicao].empilhar(eng)
        return estoque
    except Exception as e:
        print(f"[ERRO] Falha ao carregar estoque: {e}")
        return estoque
