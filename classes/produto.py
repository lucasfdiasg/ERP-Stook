# Classe Produto para instanciar um objeto de produto
class Produto:
    def __init__(self, codigo: str, nome: str, peso: str, fabricante: str, categoria: str):
        self.codigo = codigo
        self.nome = nome
        self.peso = peso  # Mantém como string, conversão é feita fora quando necessário
        self.fabricante = fabricante
        self.categoria = categoria

    def __repr__(self):
        return f"Produto('{self.codigo}', '{self.nome}', {self.peso} kg)"
