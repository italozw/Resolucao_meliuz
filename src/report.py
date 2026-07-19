"""
report.py

Responsável pela geração dos relatórios da análise.
Consome o DICT estruturado da IA (dados_ia) + o texto de métricas (resumo_metricas).
"""

import os
import html
from datetime import datetime


class Report:
    def __init__(self):
        self.pasta = "reports"
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta)

    # ---------- helpers de renderização a partir do dict ----------
    def _lista_md(self, itens):
        return "\n".join(f"- {i}" for i in itens) or "- Não especificado"

    def _lista_html(self, itens):
        li = "".join(f"<li>{html.escape(str(i))}</li>" for i in itens)
        return f"<ul>{li}</ul>" if li else "<p>Não especificado</p>"

    # ---------- Markdown ----------
    def salvar_markdown(self, parceiro, resumo_metricas, dados_ia):
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        nome = parceiro.replace(".csv", "")
        arquivo = os.path.join(self.pasta, f"{nome}.md")

        d = dados_ia
        fence = "```"  # backticks em variável => a cópia não os corrompe

        bloco_metricas = f"{fence}\n{resumo_metricas}\n{fence}"

        conteudo = f"""# Relatório de Teste A/B

**Parceiro:** {parceiro}
**Data da análise:** {data}
**Grupo recomendado pela IA:** {d.get('grupo_recomendado', 'N/A')}
**Nível de confiança:** {d.get('confianca', 'N/A')}

---

## Resumo Estatístico

{bloco_metricas}

## Recomendação da IA

{d.get('resumo', 'Não disponível.')}

### Motivos
{self._lista_md(d.get('motivos', []))}

### Riscos / Pontos de atenção
{self._lista_md(d.get('riscos', []))}
"""
        if d.get("_texto_livre"):
            bloco_livre = f"{fence}\n{d['_texto_livre']}\n{fence}"
            conteudo += f"""
### Resposta bruta da IA (parse não estruturado)

{bloco_livre}
"""
        conteudo += "\n---\nRelatório gerado automaticamente pelo sistema.\n"

        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return arquivo

    def salvar_html(self, parceiro, resumo_metricas, dados_ia):
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        nome = parceiro.replace(".csv", "")
        arquivo = os.path.join(self.pasta, f"{nome}.html")

        d = dados_ia
        html_doc = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Relatório A/B - {html.escape(parceiro)}</title>
<style>
body{{font-family:Arial;margin:40px;background:#F5F5F5;}}
.container{{background:white;padding:30px;border-radius:10px;box-shadow:0 0 8px #CCC;}}
h1{{color:#FD9CBF;}}
h2{{color:#FD9CBF;border-bottom:1px solid #DDD;padding-bottom:5px;}}
pre{{background:#EFEFEF;padding:15px;border-radius:5px;white-space:pre-wrap;}}
.veredito{{background:#FD9CBF;border-left:5px solid #FD9CBF;padding:12px;border-radius:5px;}}
.risco{{background:#FFF3E0;border-left:5px solid #FD9CBF;padding:12px;border-radius:5px;}}
</style>
</head>
<body>
<div class="container">
<h1>Relatório de Teste A/B</h1>
<p><b>Parceiro:</b> {html.escape(parceiro)}</p>
<p><b>Data:</b> {data}</p>

<div class="veredito">
  <b>🏆 Grupo recomendado:</b> {html.escape(str(d.get('grupo_recomendado', 'N/A')))}<br>
  <b>🎯 Confiança:</b> {html.escape(str(d.get('confianca', 'N/A')))}
</div>

<h2>Resumo Estatístico</h2>
<pre>{html.escape(resumo_metricas)}</pre>

<h2>Recomendação da IA</h2>
<p>{html.escape(str(d.get('resumo', 'Não disponível.')))}</p>

<h2>Motivos</h2>
{self._lista_html(d.get('motivos', []))}

<div class="risco">
<h2>Riscos / Pontos de atenção</h2>
{self._lista_html(d.get('riscos', []))}
</div>

<hr>
<p>Relatório gerado automaticamente pelo sistema.</p>
</div>
</body>
</html>
"""
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(html_doc)
        return arquivo

    # ---------- entrada única ----------
    def gerar(self, parceiro, resumo_metricas, dados_ia):
        return {
            "markdown": self.salvar_markdown(parceiro, resumo_metricas, dados_ia),
            "html": self.salvar_html(parceiro, resumo_metricas, dados_ia),
        }

    # ---------- opcional: abre o relatório na demo ----------
    def abrir(self, caminho):
        try:
            os.startfile(os.path.abspath(caminho))   # Windows
        except AttributeError:
            os.system(f'open "{caminho}"')           # macOS
        except Exception:
            os.system(f'xdg-open "{caminho}"')       # Linux