import json
from classes.estoque import Estoque
from classes.engradado import Engradado
from classes.espaco_armazenamento import EspacoArmazenamento

# Caminho padrão do arquivo onde o estoque será salvo/carregado
CAMINHO_ESTOQUE = "database/estoque.json"

# =======================================================
# Função para salvar o estado atual do objeto Estoque em JSON
# -------------------------------------------------------
# Parâmetro:
# - estoque: instância da classe Estoque (contendo o galpão com pilhas)
# Retorno:
# - True se salvou com sucesso, False em caso de erro
# =======================================================
def salvar_estoque(estoque: Estoque):
    dados = {}
    
    # Para cada posição do galpão (ex: A1, B3), pega a pilha de engradados
    for posicao, pilha in estoque.galpao.items():
        # Converte os objetos Engradado da pilha para dicionários
        dados[posicao] = [eng.__dict__ for eng in pilha.pilha]

    try:
        # Salva todos os dados em formato JSON com identação bonita
        with open(CAMINHO_ESTOQUE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao salvar estoque: {e}")
        return False

# =======================================================
# Função para carregar o estoque do arquivo JSON
# -------------------------------------------------------
# Retorno:
# - Uma instância de Estoque reconstruída a partir do arquivo JSON
#   ou vazia em caso de erro
# =======================================================
def carregar_estoque():
    estoque = Estoque()  # Cria uma nova instância do estoque vazio

    try:
        # Abre e carrega os dados salvos do arquivo
        with open(CAMINHO_ESTOQUE, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Para cada posição (ex: A2), reconstrói a pilha com objetos Engradado
        for posicao, lista_engradados in dados.items():
            for eng_dict in lista_engradados:
                eng = Engradado(**eng_dict)  # Cria objeto Engradado com os dados
                estoque.galpao[posicao].empilhar(eng)  # Empilha no local correto

        return estoque
    except Exception as e:
        print(f"[ERRO] Falha ao carregar estoque: {e}")
        return estoque  # Retorna o estoque vazio, mas funcional
