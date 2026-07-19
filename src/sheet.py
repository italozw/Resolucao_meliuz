"""
sheet.py

Responsável por registrar o histórico das análises.
"""

import csv
import os
from datetime import datetime


class Sheet:

    def __init__(self):
        self.pasta = "reports"
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta)

        self.arquivo = os.path.join(
            self.pasta,
            "historico.csv"
        )
        self.criar_planilha()

    def criar_planilha(self):
        if os.path.exists(self.arquivo):
            return

        with open(
            self.arquivo,
            "w",
            newline="",
            encoding="utf-8-sig"          # BOM: Excel lê acentos certo
        ) as csvfile:
            writer = csv.writer(csvfile, delimiter=";")   # ; = separador do Excel pt-BR
            writer.writerow([
                "Data",
                "Parceiro",
                "Grupo Recomendado",
                "GMV",
                "Cashback",
                "Comissão",
                "Receita",
                "Ticket Médio",
                "Relatório"
            ])

    def salvar(self, parceiro, grupo, dados, relatorio):
        with open(
            self.arquivo,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow([
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                parceiro,
                grupo,
                f"{dados.get('gmv', 0):.2f}",
                f"{dados.get('cashback', 0):.2f}",
                f"{dados.get('comissao', 0):.2f}",
                f"{dados.get('receita', 0):.2f}",
                f"{dados.get('ticket_medio', 0):.2f}",
                relatorio
            ])

    def listar(self):
        historico = []
        with open(
            self.arquivo,
            encoding="utf-8-sig"
        ) as csvfile:
            leitor = csv.DictReader(csvfile, delimiter=";")   # mesmo separador na leitura
            for linha in leitor:
                historico.append(linha)
        return historico