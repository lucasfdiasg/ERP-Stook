from datetime import datetime

# Classe criada para registrar um pedido
class Pedido:
    def __init__(self, nome_solicitante, id_pedido):  # <- Inicia um novo pedido
        self.id_pedido = id_pedido
        self.nome_solicitante = nome_solicitante
        # A data é registrada no momento em que o pedido é criado
        self.data_solicitacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.itens = []  # Lista para armazenar os produtos do pedido

    def adicionar_item(self, codigo_produto, quantidade):  # <- Adiciona itens ao pedido
        # Verificamos se a quantidade é um número válido
        try:
            qtde = int(quantidade)
            if qtde <= 0:
                print("[!] A quantidade deve ser um número positivo.")
                return False
            self.itens.append({
                "codigo_produto": codigo_produto,
                "quantidade": qtde
            })
            return True
        except ValueError:
            print("[!] Quantidade inválida. Por favor, insira um número.")
            return False
    # O método to_dict foi movido para DENTRO da classe
    def to_dict(self):
        return {
            "id_pedido": self.id_pedido,
            "nome_solicitante": self.nome_solicitante,
            "data_solicitacao": self.data_solicitacao,
            "itens": self.itens
        }

    def __repr__(self):
        # A segunda declaração de __repr__ foi removida.
        return f"Pedido '{self.id_pedido}' de {self.nome_solicitante} com {len(self.itens)} item(ns)."