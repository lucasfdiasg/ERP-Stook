class EspacoArmazenamento:
    def __init__(self):
        self.pilha = []  # LIFO

    def empilhar(self, engradado):
        if len(self.pilha) >= 5:
            print("[!] Pilha cheia. Não é possível adicionar mais engradados.")
            return False
        self.pilha.append(engradado)
        return True

    def desempilhar(self):
        if not self.pilha:
            print("[!] Pilha vazia.")
            return None
        return self.pilha.pop()

    def topo(self):
        if not self.pilha:
            return None
        return self.pilha[-1]

    def esta_vazia(self):
        return len(self.pilha) == 0

    def __repr__(self):
        return f"{len(self.pilha)} engradados"
