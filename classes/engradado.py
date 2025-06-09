# Classe engradado para criar um objeto engradado
class Engradado:
    def __init__(self, codigo_produto, quantidade, lote, validade, fabricacao, preco_compra, preco_venda, fornecedor):
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        self.lote = lote
        self.validade = validade
        self.fabricacao = fabricacao
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor

    def to_dict(self):
        # Retorna o engradado em formato serializável (usado para salvar em JSON)
        return {
            "codigo_produto": self.codigo_produto,
            "quantidade": self.quantidade,
            "lote": self.lote,
            "validade": self.validade,
            "fabricacao": self.fabricacao,
            "preco_compra": self.preco_compra,
            "preco_venda": self.preco_venda,
            "fornecedor": self.fornecedor
        }

    def __repr__(self):
        return f"Engradado de '{self.codigo_produto}' | {self.quantidade} itens | Lote: {self.lote}"
