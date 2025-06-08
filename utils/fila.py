# Em ERP-Stook/utils/fila.py

import collections

class Fila:
    def __init__(self):
        # O deque é uma lista duplamente encadeada, ideal para filas
        self._elementos = collections.deque()

    def enfileirar(self, elemento):
        """Adiciona um elemento ao final da fila."""
        self._elementos.append(elemento)

    def desenfileirar(self):
        """Remove e retorna o primeiro elemento da fila."""
        if self.esta_vazia():
            return None
        return self._elementos.popleft()

    def primeiro(self):
        """Retorna o primeiro elemento da fila sem removê-lo."""
        if self.esta_vazia():
            return None
        return self._elementos[0]

    def esta_vazia(self):
        """Verifica se a fila está vazia."""
        return len(self._elementos) == 0

    def __len__(self):
        """Retorna o número de elementos na fila."""
        return len(self._elementos)