class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console

    # def __str__(self):
    #     return f"Jogo: {self.nome} - Categoria: {self.categoria} - Console: {self.console}"

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha