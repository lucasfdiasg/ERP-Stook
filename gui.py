import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Canvas
from datetime import datetime

# Importando a lógica de negócio e persistência de dados do projeto original
from utils.manipulador_json import carregar_json, salvar_json
from utils.estoque_persistencia import carregar_estoque, salvar_estoque
from utils.pedidos_persistencia import carregar_fila_pedidos, salvar_fila_pedidos, registrar_pedido_processado
from classes.engradado import Engradado
from classes.pedido import Pedido
from classes.categorias import carregar_categorias, salvar_categorias

# --- Classe Principal da Aplicação ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("STOOK - Sistema de Gerenciamento de Estoque")
        self.geometry("800x600")

        # Configura o estilo para os widgets (aparência mais moderna)
        style = ttk.Style(self)
        style.theme_use("clam") # Outras opções: 'alt', 'default', 'classic'

        # Frame principal para os botões
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Título da Interface
        title_label = ttk.Label(main_frame, text="STOOK V2.1 - Painel Principal", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        # Grid para os botões do menu
        button_grid = ttk.Frame(main_frame)
        button_grid.pack(pady=10)

        # Botões do Menu Principal
        buttons = {
            "Gerenciar Produtos": self.open_product_manager,
            "Criar Engradado": self.open_create_engradado,
            "Armazenar Engradado": self.open_store_engradado,
            "Gerenciar Pedidos": self.open_order_manager,
            "Visualizar Estoque": self.open_stock_viewer,
            "Remover do Estoque": self.open_remove_from_stock,
            "Relatórios": self.open_reports_menu,
            "Histórico de Pedidos": self.open_order_history
        }

        # Cria e posiciona os botões no grid
        row, col = 0, 0
        for text, command in buttons.items():
            button = ttk.Button(button_grid, text=text, command=command, width=25)
            button.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col > 1:
                col = 0
                row += 1

    # --- Funções para Abrir Janelas de Funcionalidades ---

    def open_product_manager(self):
        """Abre a janela de gerenciamento de produtos."""
        ProductManagerWindow(self)

    def open_create_engradado(self):
        """Abre a janela para criar um novo engradado."""
        CreateEngradadoWindow(self)
        
    def open_store_engradado(self):
        """Abre a janela para armazenar um engradado existente."""
        StoreEngradadoWindow(self)

    def open_stock_viewer(self):
        """Abre a janela de visualização gráfica do estoque."""
        StockViewerWindow(self)

    def open_remove_from_stock(self):
        """Abre a janela para remover um engradado do estoque."""
        RemoveFromStockWindow(self)

    def open_order_manager(self):
        """Abre o gerenciador de pedidos."""
        OrderManagerWindow(self)
        
    def open_reports_menu(self):
        """Abre a janela de relatórios."""
        ReportsWindow(self)

    def open_order_history(self):
        """Abre a janela do histórico de pedidos."""
        OrderHistoryWindow(self)


# --- Janelas de Funcionalidades (Toplevel) ---

class ProductManagerWindow(Toplevel):
    """Janela para CRUD de Produtos."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Gerenciador de Produtos")
        self.geometry("800x500")

        # Frame de botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Cadastrar Novo", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Atualizar Selecionado", command=self.edit_product).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Remover Selecionado", command=self.delete_product).pack(side="left", padx=5)

        # Treeview para listar produtos
        cols = ("codigo", "nome", "peso", "fabricante", "categoria")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)
        self.load_products()

    def load_products(self):
        # Limpa a árvore
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Carrega e exibe os produtos
        produtos = carregar_json("database/produtos.json")
        categorias = carregar_json("database/categorias.json")
        for codigo, info in produtos.items():
            cat_nome = categorias.get(info.get('categoria', ''), 'N/A')
            self.tree.insert("", "end", values=(
                codigo,
                info.get('nome', ''),
                info.get('peso', ''),
                info.get('fabricante', ''),
                cat_nome
            ))

    def get_selected_code(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um produto na lista primeiro.")
            return None
        return self.tree.item(selected_item)['values'][0]

    def add_product(self):
        # Passa 'self' como master e a função de recarregar como callback
        AddEditProductWindow(self, self.load_products)

    def edit_product(self):
        codigo = self.get_selected_code()
        if codigo:
            AddEditProductWindow(self, self.load_products, product_code=codigo)

    def delete_product(self):
        codigo = self.get_selected_code()
        if codigo:
            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o produto {codigo}?"):
                produtos = carregar_json("database/produtos.json")
                if codigo in produtos:
                    del produtos[codigo]
                    if salvar_json("database/produtos.json", produtos):
                        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
                        self.load_products()
                    else:
                        messagebox.showerror("Erro", "Falha ao salvar o arquivo de produtos.")


class AddEditProductWindow(Toplevel):
    """Janela para adicionar ou editar um produto."""
    def __init__(self, master, callback, product_code=None):
        super().__init__(master)
        self.callback = callback
        self.product_code = product_code
        self.title("Adicionar Produto" if not product_code else "Editar Produto")
        
        self.produtos = carregar_json("database/produtos.json")
        self.categorias = carregar_categorias()
        
        # Campos do formulário
        self.entries = {}
        fields = ["codigo", "nome", "peso", "fabricante"]
        
        for i, field in enumerate(fields):
            ttk.Label(self, text=field.capitalize()).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(self, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
            
        # Campo de Categoria (Combobox)
        ttk.Label(self, text="Categoria").grid(row=len(fields), column=0, padx=10, pady=5, sticky="w")
        self.cat_combobox = ttk.Combobox(self, values=list(self.categorias.values()), state="readonly")
        self.cat_combobox.grid(row=len(fields), column=1, padx=10, pady=5, sticky="ew")
        self.entries["categoria"] = self.cat_combobox

        # Preenche os campos se for edição
        if self.product_code:
            self.entries['codigo'].config(state="disabled")
            product_data = self.produtos.get(self.product_code, {})
            self.entries['codigo'].insert(0, self.product_code)
            self.entries['nome'].insert(0, product_data.get('nome', ''))
            self.entries['peso'].insert(0, product_data.get('peso', ''))
            self.entries['fabricante'].insert(0, product_data.get('fabricante', ''))
            
            cat_key = product_data.get('categoria')
            if cat_key:
                self.cat_combobox.set(self.categorias.get(cat_key, ''))

        ttk.Button(self, text="Salvar", command=self.save).grid(row=len(fields)+1, column=0, columnspan=2, pady=20)

    def save(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        
        if not all([data['codigo'], data['nome'], data['peso'], data['fabricante'], data['categoria']]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        # Pega a chave da categoria a partir do nome
        cat_key = [key for key, value in self.categorias.items() if value == data['categoria']][0]
        
        new_product_data = {
            "nome": data['nome'],
            "peso": data['peso'],
            "fabricante": data['fabricante'],
            "categoria": cat_key
        }

        # Lógica de salvar (novo ou edição)
        if self.product_code: # Edição
            self.produtos[self.product_code] = new_product_data
        else: # Novo
            if data['codigo'] in self.produtos:
                messagebox.showerror("Erro", "Código de produto já existe.")
                return
            self.produtos[data['codigo']] = new_product_data

        if salvar_json("database/produtos.json", self.produtos):
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
            self.callback() # Atualiza a lista na janela principal
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao salvar o produto.")


class CreateEngradadoWindow(Toplevel):
    """Janela para criar um novo engradado."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Criar Novo Engradado")
        
        self.produtos = carregar_json("database/produtos.json")
        if not self.produtos:
            messagebox.showerror("Erro", "Nenhum produto cadastrado. Cadastre um produto primeiro.", parent=self)
            self.destroy()
            return
            
        self.entries = {}
        fields = {
            "codigo_produto": "Código do Produto (use o combobox)",
            "quantidade": "Quantidade de Itens",
            "lote": "Lote",
            "validade": "Validade (dd/mm/aaaa)",
            "fabricacao": "Fabricação (dd/mm/aaaa)",
            "preco_compra": "Preço de Compra (ex: 12.50)",
            "preco_venda": "Preço de Venda (ex: 19.99)",
            "fornecedor": "Fornecedor"
        }

        # Combobox para selecionar o produto
        ttk.Label(self, text="Produto").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        product_names = [f"{code} - {info['nome']}" for code, info in self.produtos.items()]
        self.product_combo = ttk.Combobox(self, values=product_names, state="readonly", width=38)
        self.product_combo.grid(row=0, column=1, padx=10, pady=5)
        self.entries['codigo_produto'] = self.product_combo

        # Demais campos
        i = 1
        for key, label in list(fields.items())[1:]:
            ttk.Label(self, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(self, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[key] = entry
            i += 1

        ttk.Button(self, text="Criar Engradado", command=self.create).grid(row=i, columnspan=2, pady=20)

    def create(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        
        # Extrai o código do produto do combobox
        if data['codigo_produto']:
            data['codigo_produto'] = data['codigo_produto'].split(' - ')[0]
        
        if not all(data.values()):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
            return
            
        try:
            # Validações básicas
            int(data['quantidade'])
            float(data['preco_compra'])
            float(data['preco_venda'])
            datetime.strptime(data['validade'], "%d/%m/%Y")
            datetime.strptime(data['fabricacao'], "%d/%m/%Y")
        except ValueError as e:
            messagebox.showerror("Erro de Formato", f"Campo inválido: {e}. Verifique os formatos de número e data.", parent=self)
            return

        engradado_obj = Engradado(**data)
        
        caminho = "database/engradados.json"
        engradados = carregar_json(caminho)
        novo_id = f"ENG{str(len(engradados) + 1).zfill(3)}"
        engradados[novo_id] = engradado_obj.to_dict()

        if salvar_json(caminho, engradados):
            messagebox.showinfo("Sucesso", f"Engradado criado e salvo com ID: {novo_id}", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao salvar o engradado.", parent=self)


class StoreEngradadoWindow(Toplevel):
    """Janela para escolher um engradado e uma posição no estoque."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Armazenar Engradado no Estoque")
        self.geometry("700x500")

        self.engradados_disponiveis = carregar_json("database/engradados.json")
        self.produtos = carregar_json("database/produtos.json")
        self.estoque = carregar_estoque()

        if not self.engradados_disponiveis:
            messagebox.showinfo("Informação", "Nenhum engradado disponível para armazenar.", parent=self)
            self.destroy()
            return

        # Frame para seleção
        selection_frame = ttk.Frame(self)
        selection_frame.pack(pady=10, padx=10, fill="x")

        # Lista de engradados
        ttk.Label(selection_frame, text="Selecione o Engradado:").pack(anchor="w")
        engradado_list = [f"{id} | {self.produtos.get(data['codigo_produto'], {}).get('nome', 'N/A')}" for id, data in self.engradados_disponiveis.items()]
        self.engradado_combo = ttk.Combobox(selection_frame, values=engradado_list, state="readonly", width=50)
        self.engradado_combo.pack(fill="x")
        self.engradado_combo.bind("<<ComboboxSelected>>", self.update_available_positions)

        # Lista de posições disponíveis
        ttk.Label(selection_frame, text="Selecione a Posição de Destino:").pack(anchor="w", pady=(10,0))
        self.posicao_combo = ttk.Combobox(selection_frame, state="readonly", width=50)
        self.posicao_combo.pack(fill="x")

        ttk.Button(self, text="Armazenar", command=self.store).pack(pady=20)

    def update_available_positions(self, event=None):
        selection = self.engradado_combo.get()
        if not selection:
            return
        
        engradado_id = selection.split(" | ")[0]
        engradado_data = self.engradados_disponiveis[engradado_id]
        codigo_produto = engradado_data['codigo_produto']

        posicoes_validas = []
        for posicao, pilha in self.estoque.galpao.items():
            if len(pilha.pilha) < 5 and (pilha.esta_vazia() or pilha.topo().codigo_produto == codigo_produto):
                produto_topo = f"Produto: {pilha.topo().codigo_produto}" if not pilha.esta_vazia() else "Vazio"
                posicoes_validas.append(f"{posicao} (Ocupado: {len(pilha.pilha)}/5) | {produto_topo}")
        
        self.posicao_combo['values'] = posicoes_validas
        if posicoes_validas:
            self.posicao_combo.set(posicoes_validas[0])
        else:
            self.posicao_combo.set("Nenhuma posição válida encontrada.")

    def store(self):
        engradado_selection = self.engradado_combo.get()
        posicao_selection = self.posicao_combo.get()

        if not engradado_selection or not posicao_selection or "Nenhuma" in posicao_selection:
            messagebox.showerror("Erro", "Selecione um engradado e uma posição válida.", parent=self)
            return
            
        engradado_id = engradado_selection.split(" | ")[0]
        destino = posicao_selection.split(" ")[0]
        
        engradado_obj = Engradado(**self.engradados_disponiveis[engradado_id])

        if self.estoque.armazenar_engradado(destino, engradado_obj):
            del self.engradados_disponiveis[engradado_id]
            salvar_json("database/engradados.json", self.engradados_disponiveis)
            salvar_estoque(self.estoque)
            messagebox.showinfo("Sucesso", f"Engradado {engradado_id} armazenado em {destino}!", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao armazenar. A posição pode estar cheia ou conter um produto diferente.", parent=self)


class StockViewerWindow(Toplevel):
    """Janela para visualização gráfica do estoque."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Visualizador de Estoque")
        self.geometry("900x750")

        self.estoque = carregar_estoque()
        self.produtos = carregar_json("database/produtos.json")

        # Canvas para desenhar o layout
        canvas = Canvas(self, bg="lightgrey")
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame para a legenda
        legend_frame = ttk.Frame(self, width=250)
        legend_frame.pack(side="right", fill="y", padx=10, pady=10)
        ttk.Label(legend_frame, text="Legenda", font=("Helvetica", 12, "bold")).pack(anchor="w")

        # Desenha o grid e preenche a legenda
        self.draw_stock_layout(canvas, legend_frame)

    def draw_stock_layout(self, canvas, legend_frame):
        cell_width, cell_height = 80, 50
        padding = 10
        produtos_em_estoque = {}

        # Cores para diferentes produtos
        colors = ["lightblue", "lightgreen", "lightcoral", "lightgoldenrodyellow", "plum", "lightpink", "cyan"]
        product_colors = {}
        color_idx = 0

        for i, col in enumerate("ABCDE"):
            for j, row in enumerate(range(1, 9)):
                pos = f"{col}{row}"
                pilha = self.estoque.galpao[pos]
                
                x1 = i * (cell_width + padding) + padding
                y1 = j * (cell_height + padding) + padding
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                fill_color = "white"
                outline_color = "black"

                if not pilha.esta_vazia():
                    cod_produto = pilha.topo().codigo_produto
                    if cod_produto not in product_colors:
                        product_colors[cod_produto] = colors[color_idx % len(colors)]
                        color_idx += 1
                    
                    fill_color = product_colors[cod_produto]
                    produtos_em_estoque[cod_produto] = self.produtos.get(cod_produto, {}).get("nome", "Desconhecido")
                
                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color, width=2)
                canvas.create_text(x1 + cell_width / 2, y1 + 15, text=pos, font=("Helvetica", 10, "bold"))
                canvas.create_text(x1 + cell_width / 2, y1 + 35, text=f"{len(pilha.pilha)}/5", font=("Helvetica", 9))

        # Adiciona a legenda de cores
        for cod, nome in produtos_em_estoque.items():
            color = product_colors[cod]
            f = ttk.Frame(legend_frame)
            f.pack(anchor="w", fill="x", pady=2)
            Canvas(f, width=20, height=20, bg=color).pack(side="left")
            ttk.Label(f, text=f" {cod}: {nome}", wraplength=180).pack(side="left", fill="x")

class RemoveFromStockWindow(Toplevel):
    """Janela para remover o engradado do topo de uma pilha."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Remover Engradado do Estoque")
        
        self.estoque = carregar_estoque()
        posicoes_ocupadas = [pos for pos, pilha in self.estoque.galpao.items() if not pilha.esta_vazia()]

        if not posicoes_ocupadas:
            messagebox.showinfo("Informação", "O estoque está vazio.", parent=self)
            self.destroy()
            return
            
        ttk.Label(self, text="Selecione a posição para remover o engradado do topo:").pack(padx=10, pady=10)
        
        self.posicao_combo = ttk.Combobox(self, values=posicoes_ocupadas, state="readonly", width=30)
        self.posicao_combo.pack(padx=10, pady=5)
        
        ttk.Button(self, text="Remover", command=self.remove).pack(pady=20)

    def remove(self):
        posicao = self.posicao_combo.get()
        if not posicao:
            messagebox.showerror("Erro", "Selecione uma posição.", parent=self)
            return

        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o engradado do topo da posição {posicao}?"):
            engradado_removido = self.estoque.remover_engradado(posicao)
            if engradado_removido:
                if salvar_estoque(self.estoque):
                    messagebox.showinfo("Sucesso", f"Engradado do produto {engradado_removido.codigo_produto} removido de {posicao}.", parent=self)
                    self.destroy()
                else:
                    messagebox.showerror("Erro", "Falha ao salvar o estado do estoque.", parent=self)
            else:
                 messagebox.showerror("Erro", "Falha ao remover o engradado.", parent=self)


class OrderManagerWindow(Toplevel):
    """Janela para gerenciar pedidos."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Gerenciador de Pedidos")
        self.geometry("800x600")

        # Botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Registrar Novo Pedido", command=self.register_order).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Processar Próximo Pedido", command=self.process_order).pack(side="left", padx=5)

        # Visualização da Fila
        ttk.Label(self, text="Fila de Pedidos Pendentes", font=("Helvetica", 12, "bold")).pack(pady=(10,0))
        self.text_area = tk.Text(self, height=20, width=90, state="disabled", wrap="word")
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.load_queue()

    def load_queue(self):
        self.text_area.config(state="normal")
        self.text_area.delete(1.0, "end")
        
        fila = carregar_fila_pedidos()
        if fila.esta_vazia():
            self.text_area.insert("end", "Fila de pedidos está vazia.")
        else:
            for idx, pedido in enumerate(fila._elementos, 1):
                pedido_info = (
                    f"[{idx}] Pedido ID: {pedido.id_pedido}\n"
                    f"    Solicitante: {pedido.nome_solicitante}\n"
                    f"    Data: {pedido.data_solicitacao}\n"
                    f"    Itens:\n"
                )
                for item in pedido.itens:
                    pedido_info += f"      - {item['codigo_produto']}: {item['quantidade']} engradado(s)\n"
                pedido_info += "-"*50 + "\n\n"
                self.text_area.insert("end", pedido_info)
        
        self.text_area.config(state="disabled")

    def register_order(self):
        RegisterOrderWindow(self, self.load_queue)

    def process_order(self):
        # A lógica de `processar_pedido` do seu arquivo de menus é complexa.
        # Vamos replicá-la aqui de forma simplificada.
        fila = carregar_fila_pedidos()
        if fila.esta_vazia():
            messagebox.showinfo("Fila Vazia", "Não há pedidos para processar.", parent=self)
            return

        if not messagebox.askyesno("Confirmar", "Deseja processar o próximo pedido da fila?"):
            return

        pedido = fila.primeiro() # Apenas verificamos, não removemos ainda
        estoque = carregar_estoque()
        
        # Lógica de verificação de estoque
        pode_atender = True
        faltantes_msg = ""
        estoque_disponivel = {}
        for pos, pilha in estoque.galpao.items():
            if not pilha.esta_vazia():
                cod = pilha.topo().codigo_produto
                estoque_disponivel[cod] = estoque_disponivel.get(cod, 0) + len(pilha.pilha)

        for item in pedido.itens:
            cod = item["codigo_produto"]
            qtd_pedida = int(item["quantidade"])
            if estoque_disponivel.get(cod, 0) < qtd_pedida:
                pode_atender = False
                faltam = qtd_pedida - estoque_disponivel.get(cod, 0)
                faltantes_msg += f"- Faltam {faltam} engradado(s) de {cod}\n"

        if not pode_atender:
            messagebox.showerror("Estoque Insuficiente", f"Não é possível atender o pedido {pedido.id_pedido}.\n{faltantes_msg}", parent=self)
            return
        
        # Se pode atender, processa de verdade
        pedido_processado = fila.desenfileirar()
        
        for item in pedido_processado.itens:
            codigo = item["codigo_produto"]
            quantidade_a_retirar = int(item["quantidade"])
            retirados = 0
            
            # Percorre o galpão para retirar os itens (dos topos das pilhas)
            for pos in sorted(estoque.galpao.keys()): # Ordena para ter consistência
                pilha = estoque.galpao[pos]
                while not pilha.esta_vazia() and pilha.topo().codigo_produto == codigo and retirados < quantidade_a_retirar:
                    estoque.remover_engradado(pos)
                    retirados += 1
        
        salvar_estoque(estoque)
        salvar_fila_pedidos(fila)
        registrar_pedido_processado(pedido_processado, completo=True)
        messagebox.showinfo("Sucesso", f"Pedido {pedido_processado.id_pedido} processado com sucesso!", parent=self)
        self.load_queue()


class RegisterOrderWindow(Toplevel):
    """Janela para registrar um novo pedido."""
    def __init__(self, master, callback):
        super().__init__(master)
        self.title("Registrar Novo Pedido")
        self.geometry("500x400")
        self.callback = callback
        self.itens_pedido = []

        self.produtos_disponiveis = self.get_available_products()

        if not self.produtos_disponiveis:
            messagebox.showinfo("Sem Estoque", "Nenhum produto disponível no estoque para criar pedidos.", parent=self)
            self.destroy()
            return

        # Formulário
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(form_frame, text="Nome do Solicitante:").grid(row=0, column=0, sticky="w")
        self.solicitante_entry = ttk.Entry(form_frame, width=30)
        self.solicitante_entry.grid(row=0, column=1, sticky="ew")

        # Adicionar itens
        item_frame = ttk.LabelFrame(self, text="Adicionar Itens ao Pedido")
        item_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ttk.Label(item_frame, text="Produto:").grid(row=0, column=0)
        self.prod_combo = ttk.Combobox(item_frame, values=list(self.produtos_disponiveis.keys()), state="readonly")
        self.prod_combo.grid(row=0, column=1)

        ttk.Label(item_frame, text="Qtd. Engradados:").grid(row=1, column=0)
        self.qtd_spinbox = ttk.Spinbox(item_frame, from_=1, to=100)
        self.qtd_spinbox.grid(row=1, column=1)
        
        ttk.Button(item_frame, text="Adicionar Item", command=self.add_item).grid(row=2, columnspan=2, pady=5)
        
        # Itens adicionados
        self.itens_listbox = tk.Listbox(item_frame)
        self.itens_listbox.grid(row=3, columnspan=2, sticky="ew", pady=5)

        ttk.Button(self, text="Registrar Pedido", command=self.save_order).pack(pady=10)

    def get_available_products(self):
        estoque = carregar_estoque()
        produtos = carregar_json("database/produtos.json")
        disponiveis = {}
        for pos, pilha in estoque.galpao.items():
            if not pilha.esta_vazia():
                cod = pilha.topo().codigo_produto
                disponiveis[f"{cod} - {produtos.get(cod, {}).get('nome', 'N/A')}"] = cod
        return disponiveis

    def add_item(self):
        produto_selecionado = self.prod_combo.get()
        quantidade = self.qtd_spinbox.get()
        if not produto_selecionado or not quantidade:
            return
            
        cod_produto = self.produtos_disponiveis[produto_selecionado]
        self.itens_pedido.append({"codigo_produto": cod_produto, "quantidade": int(quantidade)})
        self.itens_listbox.insert("end", f"{quantidade} engradado(s) de {produto_selecionado}")

    def save_order(self):
        solicitante = self.solicitante_entry.get()
        if not solicitante:
            messagebox.showerror("Erro", "Nome do solicitante é obrigatório.", parent=self)
            return
        if not self.itens_pedido:
            messagebox.showerror("Erro", "Adicione pelo menos um item ao pedido.", parent=self)
            return
            
        fila_pedidos = carregar_fila_pedidos()
        novo_id = f"PED{len(fila_pedidos._elementos) + len(carregar_json('database/historico_pedidos.json')) + 1:03d}"
        
        novo_pedido = Pedido(solicitante, novo_id)
        novo_pedido.itens = self.itens_pedido
        
        fila_pedidos.enfileirar(novo_pedido)
        if salvar_fila_pedidos(fila_pedidos):
            messagebox.showinfo("Sucesso", f"Pedido {novo_id} registrado com sucesso!", parent=self)
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao salvar o pedido.", parent=self)

class ReportsWindow(Toplevel):
    """Janela para exibir relatórios."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatórios")
        self.geometry("700x500")

        # Frame de botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, fill='x', padx=10)
        ttk.Button(btn_frame, text="Produtos Próximos do Vencimento", command=self.show_expiring_products).pack(fill='x')
        ttk.Button(btn_frame, text="Itens em Falta para Pedidos", command=self.show_missing_items).pack(fill='x', pady=5)

        # Área de texto para exibir o relatório
        self.report_text = tk.Text(self, state="disabled", wrap="word", font=("Courier New", 10))
        self.report_text.pack(expand=True, fill="both", padx=10, pady=10)

    def _display_report(self, title, content):
        self.report_text.config(state="normal")
        self.report_text.delete(1.0, "end")
        self.report_text.insert("end", f"{title}\n{'='*len(title)}\n\n{content}")
        self.report_text.config(state="disabled")

    def show_expiring_products(self):
        estoque = carregar_estoque()
        hoje = datetime.now()
        report_content = ""

        for pos, pilha in estoque.galpao.items():
            for engradado in pilha.pilha:
                try:
                    validade = datetime.strptime(engradado.validade, "%d/%m/%Y")
                    dias_para_vencer = (validade - hoje).days
                    if 0 <= dias_para_vencer <= 30:
                        report_content += (
                            f"⚠️ Produto: {engradado.codigo_produto}\n"
                            f"   Lote: {engradado.lote}\n"
                            f"   Validade: {engradado.validade} (Vence em {dias_para_vencer} dia(s))\n"
                            f"   Localização: {pos}\n"
                            f"------------------------------------\n"
                        )
                except ValueError:
                    continue # Ignora engradados com data inválida
        
        if not report_content:
            report_content = "Nenhum produto vencendo nos próximos 30 dias."
        
        self._display_report("Produtos Próximos do Vencimento (30 dias)", report_content)

    def show_missing_items(self):
        fila_pedidos = carregar_fila_pedidos()
        estoque = carregar_estoque()
        produtos = carregar_json("database/produtos.json")
        report_content = ""

        if fila_pedidos.esta_vazia():
            report_content = "✅ Nenhum pedido pendente na fila."
        else:
            # Calcula o estoque total de cada produto
            estoque_disponivel = {}
            for pilha in estoque.galpao.values():
                if not pilha.esta_vazia():
                    cod = pilha.topo().codigo_produto
                    estoque_disponivel[cod] = estoque_disponivel.get(cod, 0) + len(pilha.pilha)

            # Verifica cada pedido
            for pedido in fila_pedidos._elementos:
                itens_faltantes_msg = ""
                for item in pedido.itens:
                    cod = item["codigo_produto"]
                    qtd_pedida = item["quantidade"]
                    qtd_em_estoque = estoque_disponivel.get(cod, 0)

                    if qtd_em_estoque < qtd_pedida:
                        nome_produto = produtos.get(cod, {}).get("nome", "Desconhecido")
                        faltam = qtd_pedida - qtd_em_estoque
                        itens_faltantes_msg += f"   - Falta(m) {faltam} de {cod} ({nome_produto})\n"
                
                if itens_faltantes_msg:
                    report_content += f"🚨 Pedido {pedido.id_pedido} ({pedido.nome_solicitante}) não pode ser atendido:\n"
                    report_content += itens_faltantes_msg
                    report_content += "---------------------------------------------------------\n"
        
        if not report_content:
            report_content = "✅ Todos os pedidos na fila podem ser atendidos com o estoque atual."
            
        self._display_report("Relatório de Itens em Falta para Pedidos Pendentes", report_content)


class OrderHistoryWindow(Toplevel):
    """Janela para visualizar o histórico de pedidos processados."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Histórico de Pedidos")
        self.geometry("700x500")

        # Área de texto para exibir o histórico
        self.history_text = tk.Text(self, state="disabled", wrap="word")
        self.history_text.pack(expand=True, fill="both", padx=10, pady=10)
        self.load_history()

    def load_history(self):
        historico = carregar_json("database/historico_pedidos.json")
        history_content = ""

        if not historico:
            history_content = "Nenhum pedido no histórico."
        else:
            for pedido_id, dados in historico.items():
                status = '✅ Completo' if dados.get('status') == 'Completo' else '⚠️ Parcial'
                history_content += (
                    f"🧾 Pedido ID: {pedido_id}\n"
                    f"👤 Solicitante: {dados['solicitante']}\n"
                    f"📦 Status: {status}\n"
                    f"Engradados pedidos:\n"
                )
                for item in dados["itens"]:
                    history_content += f" - {item['codigo_produto']}: {item['quantidade']} engradado(s)\n"
                history_content += f"{'-'*50}\n\n"

        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        self.history_text.insert("end", history_content)
        self.history_text.config(state="disabled")

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    app = App()
    app.mainloop()