import json
import os

# Função para salvar qualquer dicionário como JSON
def salvar_json(caminho_arquivo, dado): 
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dado, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERRO] Ao salvar arquivo: {e}")
        return False
# Função para carregar um arquivo JSON
def carregar_json(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return {}  # Arquivo ainda não existe
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRO] Ao carregar arquivo: {e}")
        return {}
