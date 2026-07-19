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

    # -------------------------------------------------------

    def criar_planilha(self):

        """
        Cria o arquivo caso ele não exista.
        """

        if os.path.exists(self.arquivo):
            return

        with open(
            self.arquivo,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

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

    # -------------------------------------------------------

    def salvar(
        self,
        parceiro,
        grupo,
        dados,
        relatorio
    ):

        """
        Registra uma nova análise.
        """

        with open(
            self.arquivo,
            "a",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow([

                datetime.now().strftime("%d/%m/%Y %H:%M"),

                parceiro,

                grupo,

                f"{dados['gmv']:.2f}",

                f"{dados['cashback']:.2f}",

                f"{dados['comissao']:.2f}",

                f"{dados['receita']:.2f}",

                f"{dados['ticket_medio']:.2f}",

                relatorio

            ])

    # -------------------------------------------------------

    def listar(self):

        """
        Retorna todo o histórico.
        """

        historico = []

        with open(
            self.arquivo,
            encoding="utf-8"
        ) as csvfile:

            leitor = csv.DictReader(csvfile)

            for linha in leitor:
                historico.append(linha)

        return historico