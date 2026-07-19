import re

class Analyzer:
    def __init__(self, dados):
        self.dados = dados
        self.colunas = {}

    def localizar_colunas(self):
        self.colunas = {}
        if not self.dados:
            return
        
        exemplo = self.dados[0]

        for coluna in exemplo.keys():
            nome = coluna.lower()

            if "grupo" in nome:
                self.colunas["grupo"] = coluna
            elif any(x in nome for x in ["gmv", "receita", "total", "vendas totais"]):
                self.colunas["gmv"] = coluna
            elif "cash" in nome or "desconto" in nome:
                self.colunas["cashback"] = coluna
            elif "comiss" in nome:
                self.colunas["comissao"] = coluna
            elif any(x in nome for x in ["usuario", "user", "comprador", "cliente"]):
                self.colunas["compradores"] = coluna
            elif "venda" in nome:
                self.colunas["vendas"] = coluna

    def numero(self, valor):
        if valor is None:
            return 0
        
        valor = str(valor)

        valor = valor.replace("R$", "")
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

        valor = re.sub(r"[^0-9.-]", "", valor)

        if valor == "":
            return 0
        
        try: 
            return float(valor)
        except:
            return 0
    
    def calcular(self):
        self.localizar_colunas()

        grupo_col = self.colunas.get("grupo")

        if grupo_col is None:
            raise Exception(
                "Não foi encontrada uma coluna de grupos."
            )
        
        grupos = {}

        for linha in self.dados:
            grupo = linha[grupo_col]

            if grupo not in grupos:
                grupos[grupo] = {
                    "compradores": 0,

                    "gmv": 0,

                    "cashback": 0,

                    "comissao": 0,

                    "receita": 0,

                    "vendas": 0
                }
            if "compradores" in self.colunas:
                grupos[grupo]["compradores"] += self.numero(
                    linha[self.colunas["compradores"]]
                )
            
            if "gmv" in self.colunas:
                grupos[grupo]["gmv"] += self.numero(
                    linha[self.colunas["gmv"]]
                )

            if "cashback" in self.colunas:
                grupos[grupo]["cashback"] += self.numero(
                    linha[self.colunas["cashback"]]
                )
            
            if "comissao" in self.colunas:
                grupos[grupo]["comissao"] += self.numero(
                    linha[self.colunas["comissao"]]
                )

            if "receita" in self.colunas:
                grupos[grupo]["receita"] += self.numero(
                    linha[self.colunas["receita"]]
                )
            
            if "vendas" in self.colunas:
                grupos[grupo]["vendas"] += self.numero(
                    linha[self.colunas["vendas"]]
                )
        
        for grupo in grupos.values():

            if grupo["compradores"] > 0:
                grupo["ticket_medio"] = (
                    grupo["gmv"] /
                    grupo["compradores"]
                )
            else:
                grupo["ticket_medio"] = 0

        return grupos
    
    def vencedor(self):

        grupos = self.calcular()

        vencedor = None
        maior_gmv = -1

        for nome, dados in grupos.items():

            if dados["gmv"] > maior_gmv:

                maior_gmv = dados["gmv"]
                vencedor = nome

        return vencedor
    
    def resumo_para_ia(self):

        grupos = self.calcular()
        texto = ""

        for nome, dados in grupos.items():
            texto += f"""

Grupo: {nome}

Compradores: {dados['compradores']}

GMV: {dados['gmv']:.2f}

Cashback: {dados['cashback']:.2f}

Comissão: {dados['comissao']:.2f}

Receita: {dados['receita']:.2f}

Vendas: {dados['vendas']:.2f}

Ticket Médio: {dados['ticket_medio']:.2f}

"""
        texto += f"""

Grupo recomendado automaticamente:

{self.vencedor()}
"""
        return texto