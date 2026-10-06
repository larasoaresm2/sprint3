from abc import ABC, abstractmethod

class Asset(ABC):
    """Classe base abstrata: representa qualquer ativo de TI."""

    def __init__(self, id_ativo, nome, responsavel):
        self.id = id_ativo
        self.nome = nome
        self.responsavel = responsavel

    @abstractmethod
    def exibir_detalhes(self):
        """Cada tipo de ativo é obrigado a definir como se apresenta"""
        return f"[{self.id}]{self.nome} | responsável: {self.responsavel}"


class Server(Asset):
    def __init__ (self, id_ativo, nome, responsavel, sistema operacional):
        super().__init__(id_ativo, nome, responsavel)
        self.sistema_operacional = sistema operacional

    def exibir_detalhes(self):
        base = super().exibir_detalhes()
        return f"{base} | SO: {self.sistema_operacional}"


class Router(Asset):
    def __init__(self, id_ativo, nome, responsavel, modelo):
        super().__init__(id_ativo, nome, responsavel)
        self.modelo = modelo

    def exibir_detalhes(self):
        base = super().exibir_detalhes()
        return f"{base} | Modelo: {self.modelo}"    

class Notebook(Asset):
    def __init__(self, id_ativo, nome, responsavel, marca):
        super().__init__(id_ativo, nome, responsavel)
        self.marca = marca

    def exibir_detalhes(self):
        base = super().exibir_detalhes()
        return f"{base} | Marca: {self.marca}"

if __name__ == "__main__":

    Server = Server(1, "Servidor de Arquivos", "João", "Linux")
    print(Server.exibir_detalhes())


    ativos = [Server, Router, Notebook]
    pass