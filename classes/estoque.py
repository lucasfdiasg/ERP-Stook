from classes.espaco_armazenamento import EspacoArmazenamento

class Estoque:
    def __init__(self):
        # cria 40 posições: A1 até E8
        self.galpao = {
            f"{coluna}{linha}": EspacoArmazenamento()
            for coluna in "ABCDE"
            for linha in range(1, 9)
        }

    def armazenar_engradado(self, posicao, engradado):
        if posicao not in self.galpao:
            print("[!] Posição inválida.")
            return False
        return self.galpao[posicao].empilhar(engradado)

    def remover_engradado(self, posicao):
        if posicao not in self.galpao:
            print("[!] Posição inválida.")
            return None
        return self.galpao[posicao].desempilhar()

    def consultar_topo(self, posicao):
        if posicao not in self.galpao:
            print("[!] Posição inválida.")
            return None
        return self.galpao[posicao].topo()

    def visualizar_estoque(self):
        for linha in range(1, 9):
            for coluna in "ABCDE":
                pos = f"{coluna}{linha}"
                pilha = self.galpao[pos]
                print(f"{pos}: {len(pilha.pilha)} engradado(s)")
            print()
