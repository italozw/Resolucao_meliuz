"""
csv_reader.py

Responsável pela leitura do arquivo CSV.

Autor: Italo Luan de Almeida
"""

import csv
import os

class CSVReader:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.dados = []
        self.colunas = []

    def carregar(self):
        with open(self.arquivo,
                mode="r", 
                encoding="utf-8-sig") as arquivo:
        
            leitor = csv.DictReader(arquivo)

            self.colunas = leitor.fieldnames

            for linha in leitor:
                self.dados.append(linha)

        return self.dados

    def quantidade_registros(self):

        return len(self.dados)
    
    def quantidade_colunas(self):
        
        return len(self.colunas)
    
    def listar_colunas(self):
        return self.colunas
    
    def grupos(self):
        """
        Procura automaticamente a coluna que possui
        o grupo do experimento.
        """

        grupos = set()

        for linha in self.dados:

            for coluna in linha:

                nome = coluna.lower()

                if "grupo" in nome:
                    grupos.add(linha[coluna])
            
        return sorted(list(grupos))
    
    def parceiro(self):
        """
        Obtém o nome do parceiro
        através do nome do arquivo.
        """

        return os.path.basename(self.arquivo)
    
    def resumo(self):

        """
        Retorna um resumo das informações.
        """

        return {
            "arquivo": self.parceiro(),
            "registros": self.quantidade_registros(),
            "colunas": self.quantidade_colunas(),
            "grupos": self.grupos(),
            "dados": self.dados
        }