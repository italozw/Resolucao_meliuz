"""
interface.py

Responsável pela interface gráfica da aplicação.
"""

import os
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
from src.csv_reader import CSVReader
from src.analyzer import Analyzer
from src.ai import AIAnalyzer
from src.report import Report
from src.sheet import Sheet


class App:

    def __init__(self):
        self.arquivo_csv = ""
        self.leitor = None
        self.ultimo_html = None

        self.root = tk.Tk()
        self.root.title("Méliuz - A/B Teste de Analise")
        self.root.geometry("950x800")
        self.root.resizable(True, True)

        self.criar_componentes()

    def criar_componentes(self):
        titulo = tk.Label(
            self.root,
            text="Analisador de Testes A/B",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

        frame_arquivo = tk.Frame(self.root)
        frame_arquivo.pack(fill="x", padx=20)

        tk.Label(
            frame_arquivo,
            text="Arquivo CSV:",
            font=("Arial", 11)
        ).pack(anchor="w")

        linha = tk.Frame(frame_arquivo)
        linha.pack(fill="x", pady=5)

        self.entry_arquivo = tk.Entry(linha, font=("Arial", 10))
        self.entry_arquivo.pack(side="left", fill="x", expand=True)

        tk.Button(
            linha,
            text="Selecionar",
            command=self.selecionar_arquivo
        ).pack(side="left", padx=10)

        resumo = ttk.LabelFrame(self.root, text="Resumo")
        resumo.pack(fill="x", padx=20, pady=15)

        self.label_resumo = scrolledtext.ScrolledText(
            resumo, font=("Arial", 10), height=6, wrap=tk.WORD
        )
        self.label_resumo.pack(fill="both", padx=10, pady=10)
        self.label_resumo.insert(tk.END, "Parceiros:\nPeríodo:\nRegistros:\nGrupos:\n")
        self.label_resumo.config(state="disabled")

        self.botao_analisar = tk.Button(
            self.root,
            text="🚀 Iniciar Análise",
            font=("Arial", 11, "bold"),
            bg="#00695C",
            fg="white",
            padx=15,
            pady=8,
            command=self.analisar
        )
        self.botao_analisar.pack(pady=10)

        self.progress = ttk.Progressbar(
            self.root, mode="determinate", maximum=100
        )
        self.progress.pack(fill="x", padx=20, pady=5)

        frame_status = ttk.LabelFrame(self.root, text="Status")
        frame_status.pack(fill="both", padx=20, pady=10)

        self.status = scrolledtext.ScrolledText(frame_status, height=5)
        self.status.pack(fill="both", padx=10, pady=10)

        # >>> AÇÕES NO RODAPÉ: empacota ANTES do resultado (senão somem) <<<
        frame_acoes = tk.Frame(self.root)
        frame_acoes.pack(side="bottom", pady=10)

        tk.Button(
            frame_acoes,
            text="📄 Abrir Relatório",
            command=self.abrir_relatorio
        ).pack(side="left", padx=10)

        tk.Button(
            frame_acoes,
            text="🧹 Limpar",
            command=self.limpar
        ).pack(side="left", padx=10)

        # >>> RESULTADO: expande no espaço que sobrou ACIMA dos botões <<<
        resultado = ttk.LabelFrame(self.root, text="Resultado da IA")
        resultado.pack(fill="both", expand=True, padx=20, pady=10)

        self.resultado = scrolledtext.ScrolledText(resultado, font=("Consolas", 10))
        self.resultado.pack(fill="both", expand=True, padx=10, pady=10)

    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(
            title="Selecione um CSV",
            filetypes=[("Arquivos CSV", "*.csv")]
        )
        if not arquivo:
            return

        self.arquivo_csv = arquivo
        self.entry_arquivo.delete(0, tk.END)
        self.entry_arquivo.insert(0, arquivo)

        try:
            self.leitor = CSVReader(self.arquivo_csv)
            self.leitor.carregar()
            self.atualizar_resumo_interface()
            self.log(f"Arquivo carregado: {len(self.leitor.dados)} registros")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao ler CSV:\n{e}")
            self.label_resumo.config(state="normal")
            self.label_resumo.delete("1.0", tk.END)
            self.label_resumo.insert(tk.END, "Erro ao carregar arquivo")
            self.label_resumo.config(state="disabled")
            self.leitor = None

    def atualizar_resumo_interface(self):
        if not self.leitor or not self.leitor.dados:
            return

        total = self.leitor.quantidade_registros()
        grupos = self.leitor.grupos()
        nome_arquivo = self.leitor.parceiro()

        distribuicao = {}
        if grupos:
            coluna_grupo = None
            for col in self.leitor.colunas:
                if "grupo" in col.lower():
                    coluna_grupo = col
                    break
            if coluna_grupo:
                for linha in self.leitor.dados:
                    g = linha.get(coluna_grupo, 'N/A')
                    distribuicao[g] = distribuicao.get(g, 0) + 1

        texto = (
            f"Arquivo: {nome_arquivo}\n\n"
            f"Registros: {total:,}\n"
            f"Colunas: {self.leitor.quantidade_colunas()}\n"
            f"Grupos detectados: {', '.join(grupos) if grupos else 'Nenhum'}\n\n"
            f"Balanceamento:\n"
        )
        for grupo in sorted(distribuicao.keys()):
            qtd = distribuicao[grupo]
            pct = (qtd / total) * 100 if total > 0 else 0
            texto += f"  • {grupo}: {qtd:,} ({pct:.1f}%)\n"

        alertas = []
        if len(grupos) < 2:
            alertas.append("Erro: Menos de 2 grupos detectados")
        elif total < 1000:
            alertas.append("Aviso: Amostra pequena (< 1000)")
        if len(distribuicao) >= 2:
            proporcoes = [v / total for v in distribuicao.values()]
            if max(proporcoes) > 0.6:
                alertas.append("Desbalanceamento forte detectado")

        texto += ("\n" + "\n".join(alertas)) if alertas else "\nDataset válido para análise"

        self.label_resumo.config(state="normal")
        self.label_resumo.delete("1.0", tk.END)
        self.label_resumo.insert(tk.END, texto)
        self.label_resumo.config(state="disabled")

    def analisar(self):
        if not self.leitor or self.arquivo_csv == "":
            messagebox.showwarning("Aviso", "Selecione um arquivo CSV.")
            return

        # Limpa as telas antes de começar
        self.progress["value"] = 0
        self.resultado.delete("1.0", tk.END)
        self.status.delete("1.0", tk.END)
        self.botao_analisar.config(state="disabled")

        try:
            self.progress["value"] = 10
            self.log("Iniciando análise...")

            resumo = self.leitor.resumo()
            self.log(f"Registros: {resumo['registros']}, Grupos: {resumo['grupos']}")

            self.progress["value"] = 30
            self.log("Calculando métricas...")
            analyzer = Analyzer(resumo["dados"])
            resultado = analyzer.calcular()
            vencedor = analyzer.vencedor()

            texto_resumo = f"Arquivo: {resumo['arquivo']}\n\n"
            for nome, dados in resultado.items():
                texto_resumo += (
                    f"--- {nome} ---\n"
                    f"Compradores: {dados['compradores']:,.0f}\n"
                    f"GMV: R$ {dados['gmv']:,.2f}\n"
                    f"Cashback: R$ {dados['cashback']:,.2f}\n"
                    f"Ticket Médio: R$ {dados['ticket_medio']:,.2f}\n\n"
                )
            texto_resumo += f"Recomendado Automaticamente: {vencedor}"

            self.label_resumo.config(state="normal")
            self.label_resumo.delete("1.0", tk.END)
            self.label_resumo.insert(tk.END, texto_resumo)
            self.label_resumo.config(state="disabled")

            self.progress["value"] = 60
            ai = AIAnalyzer(provider="groq")
            self.log(f"Consultando IA ({ai.provider})...")
            dados_ia = ai.analisar(resultado, vencedor)
            self.dados_ia = dados_ia

            texto_final = ai.formatar_resposta(dados_ia)
            if dados_ia.get("_texto_livre"):
                texto_final += f"\n\n--- Resposta bruta da IA ---\n{dados_ia['_texto_livre']}"

            self.progress["value"] = 80
            self.log("Gerando arquivos de relatório...")
            report = Report()
            caminhos = report.gerar(
                parceiro=self.leitor.parceiro(),
                resumo_metricas=texto_resumo,
                dados_ia=dados_ia,
            )
            self.ultimo_html = caminhos["html"]
            self.log(f"✅ Markdown: {caminhos['markdown']}")
            self.log(f"✅ HTML:     {caminhos['html']}")

            self.progress["value"] = 90
            self.log("Registrando no histórico...")
            grupo_rec = dados_ia.get("grupo_recomendado") or vencedor
            metricas_grupo = resultado.get(grupo_rec, resultado[vencedor])
            try:
                sheet = Sheet()
                sheet.salvar(
                    parceiro=self.leitor.parceiro(),
                    grupo=grupo_rec,
                    dados=metricas_grupo,
                    relatorio=caminhos["html"],
                )
                self.log(f"✅ Histórico atualizado: {sheet.arquivo}")
            except Exception as e:
                self.log(f"⚠️ Falha ao gravar histórico (relatório OK): {e}")

            self.progress["value"] = 100
            self.log("✔ Processo concluído com sucesso.")
            self.log(f"Grupo recomendado pela IA: {grupo_rec}")

            # >>> DESENHA O RESULTADO UMA ÚNICA VEZ, NO FIM (sem delete depois) <<<
            self.resultado.delete("1.0", tk.END)
            self.resultado.insert(tk.END, texto_final)

            messagebox.showinfo("Concluído", "Análise finalizada com sucesso!")

        except Exception as erro:
            messagebox.showerror("Erro", f"Falha durante a análise:\n{erro}")
            self.log(f"❌ Erro: {erro}")
            # Em erro, a tela NÃO fica vazia: mostra a mensagem
            self.resultado.delete("1.0", tk.END)
            self.resultado.insert(tk.END, f"Erro na análise:\n{erro}")

        finally:
            self.botao_analisar.config(state="normal")

    def abrir_relatorio(self):
        caminho = getattr(self, "ultimo_html", None)
        if caminho and os.path.exists(caminho):
            webbrowser.open(caminho)
            return
        pasta = "reports"
        try:
            htmls = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".html")]
        except FileNotFoundError:
            htmls = []
        if htmls:
            webbrowser.open(os.path.abspath(max(htmls, key=os.path.getmtime)))
        else:
            messagebox.showinfo("Relatório", "Nenhum HTML encontrado. Rode uma análise primeiro.")

    def limpar(self):
        self.resultado.delete("1.0", tk.END)
        self.status.delete("1.0", tk.END)
        self.progress["value"] = 0

    def log(self, texto):
        self.status.insert(tk.END, texto + "\n")
        self.status.see(tk.END)

    def run(self):
        self.root.mainloop()