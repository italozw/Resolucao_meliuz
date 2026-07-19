"""
ai.py  -  IA estruturada (JSON), agnóstica de provedor, com parse blindado.
"""

import os
import re
import json
from dotenv import load_dotenv
load_dotenv(override=True)

SCHEMA_DEFAULT = {
    "grupo_recomendado": "",
    "confianca": "",
    "motivos": [],
    "riscos": [],
    "resumo": "",
}

INSTRUCAO_JSON = """
REGRA DE FORMATO (OBRIGATÓRIA):
Responda APENAS com um objeto JSON válido. Não use blocos de código (```),
não escreva nada antes ou depois. Use exatamente estas chaves:
{"grupo_recomendado":"...","confianca":"Alta|Média|Baixa",
 "motivos":["..."],"riscos":["..."],"resumo":"1-2 frases executivas"}
"""


class AIAnalyzer:
    def __init__(self, api_key=None, prompt_file="prompt.md", provider="ollama"):
        self.provider = provider

        base_dir = os.path.dirname(os.path.abspath(__file__))    
        project_root = os.path.dirname(base_dir)                 
        self.prompt_base = self._carregar_prompt(
            os.path.join(project_root, "prompts", prompt_file)
        )

        self.client = None
        if provider == "groq":
            from groq import Groq
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("GROQ_API_KEY não encontrada no .env")
            self.client = Groq(api_key=self.api_key)
            self.modelos = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

        elif provider == "gemini":
            from google import genai
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY não encontrada no .env")
            self.client = genai.Client(api_key=self.api_key)
            self.modelos = ["gemini-2.0-flash-lite", "gemini-1.5-flash"]

        elif provider == "ollama":
            import ollama 
            self.client = ollama
            self.api_key = None
            self.modelos = ["qwen2.5:3b", "llama3.2:3b"]

        else:
            raise ValueError(f"Provider desconhecido: {provider}")

    def _carregar_prompt(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ("Você é um analista sênior de growth do Méliuz. "
                    "Analise o teste A/B com foco em GMV, ticket médio e custo de cashback.")

    def _montar_prompt(self, dados_grupos, vencedor):
        texto_dados = ""
        for nome, dados in dados_grupos.items():
            texto_dados += (
                f"\nGrupo {nome}:\n"
                f"- Compradores: {dados.get('compradores', 0):,}\n"
                f"- GMV: R$ {dados.get('gmv', 0):,.2f}\n"
                f"- Cashback: R$ {dados.get('cashback', 0):,.2f}\n"
                f"- Comissão: R$ {dados.get('comissao', 0):,.2f}\n"
                f"- Ticket Médio: R$ {dados.get('ticket_medio', 0):,.2f}\n"
                f"- Vendas: {dados.get('vendas', 0):,}\n"
            )

        return (
            f"{self.prompt_base}\n{INSTRUCAO_JSON}\n"
            f"DADOS DOS GRUPOS:\n{texto_dados}\n"
            f"GRUPO COM MAIOR GMV CALCULADO: {vencedor}"
        )

    def _chamar_modelo(self, prompt):
        ultimo = None
        for modelo in self.modelos:
            try:
                if self.provider == "groq":
                    r = self.client.chat.completions.create(
                        model=modelo,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2,
                        response_format={"type": "json_object"},  
                    )
                    return r.choices[0].message.content
                if self.provider == "gemini":
                    from google.genai import types
                    r = self.client.models.generate_content(
                        model=modelo, contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"),
                    )
                    return r.text
                if self.provider == "ollama":
                    r = self.client.generate(model=modelo, prompt=prompt, format="json")
                    return r.get("response", "")
            except Exception as e:
                ultimo = e
                msg = str(e)
                if any(x in msg for x in ["429", "404", "quota", "rate",
                                          "NOT_FOUND", "RESOURCE_EXHAUSTED", "not found"]):
                    print(f"⚠️ {modelo} indisponível, tentando o próximo...")
                    continue
                break
        raise ultimo or RuntimeError("Nenhum modelo respondeu.")

    def _extrair_json(self, texto):
        if not texto:
            return None
        texto = texto.strip()
        try:
            obj = json.loads(texto)
        except json.JSONDecodeError:
            limpo = re.sub(r"^```(?:json)?", "", texto, flags=re.I).strip()
            limpo = re.sub(r"```$", "", limpo).strip()
            m = re.search(r"\{.*\}", limpo, flags=re.S)
            if not m:
                return None
            try:
                obj = json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
        if not isinstance(obj, dict):
            return None
        for k, v in SCHEMA_DEFAULT.items():
            obj.setdefault(k, [] if isinstance(v, list) else v)
        for chave in ("motivos", "riscos"):
            if not isinstance(obj[chave], list):
                obj[chave] = [str(obj[chave])]
        return obj

    def analisar(self, dados_grupos, vencedor):
        prompt = self._montar_prompt(dados_grupos, vencedor)
        try:
            texto_bruto = self._chamar_modelo(prompt)
        except Exception as e:
            print(f"⚠️ IA indisponível, usando fallback: {e}")
            return self._fallback(vencedor, f"IA indisponível ({e.__class__.__name__})")

        parsed = self._extrair_json(texto_bruto)
        if parsed is None:
            fb = self._fallback(vencedor, "IA não retornou JSON válido")
            fb["_texto_livre"] = texto_bruto   
            return fb
        return parsed

    def _fallback(self, vencedor, motivo=""):
        return {
            "grupo_recomendado": vencedor,
            "confianca": "Indisponível",
            "motivos": [f"Análise automática: {vencedor} liderou em GMV."],
            "riscos": [motivo] if motivo else [],
            "resumo": (f"Recomendação automática por GMV ({vencedor}); "
                       f"a IA não pôde complementar a análise no momento."),
        }

    def formatar_resposta(self, dados):
        motivos = "\n".join(f"• {m}" for m in dados.get("motivos", [])) or "• Não especificado"
        riscos = "\n".join(f"• {r}" for r in dados.get("riscos", [])) or "• Não especificado"
        return f"""🏆 RECOMENDAÇÃO DA IA

Grupo Recomendado: {dados.get('grupo_recomendado', 'N/A')}
Nível de Confiança: {dados.get('confianca', 'N/A')}

📊 MOTIVOS:
{motivos}

⚠️ RISCOS:
{riscos}

📋 RESUMO ESTRATÉGICO:
{dados.get('resumo', 'Não disponível.')}


Dados validados pelo sistema interno.
"""