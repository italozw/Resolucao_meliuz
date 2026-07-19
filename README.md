# 🧪 Méliuz A/B Test Analyzer v1.0

**Sistema automatizado de análise A/B com IA estruturada + geração relatórios em HTML/Markdown.**

> **Status:** ✅ Produção-Ready | **Provider IA:** Groq (gratuito) / Gemini / Ollama | **Linguagem:** Python 3.11+

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Demonstração](#demonstração)
3. [Arquitetura](#arquitetura)
4. [Funcionalidades](#funcionalidades)
5. [Instalação Rápida](#instalação-rápida)
6. [Como Usar](#como-usar)
7. [Estrutura do Projeto](#estrutura-do-projeto)
8. [Customização](#customização)
9. [Integrações](#integrações)
10. [Roadmap & Limitações](#roadmap--limitações)

---

## Visão Geral

Este projeto resolve o **Case Técnico — Estágio Ops Integradas Méliuz**: construir uma ferramenta reutilizável que recebe testes A/B de cashback, analisa via IA, e recomenda ações estratégicas sem necessidade de alterar código ao trocar datasets.

### Por que este projeto é diferente?

| Abordagem Tradicional | Este Projeto |
|------------------------|---------------|
| Analista abre CSV no Excel e calcula manualmente | Sistema lê, normaliza, valida automaticamente |
| ChatGPT "bate-papo" solta sem estrutura | **IA retorna estruturado**: `grupo_recomendado`, `confiança`, `motivos`, `riscos` |
| Planilha única desorganizada | **Histórico consolidado** em `historico.csv` + relatórios HTML individuais |
| Código "one-off" que só serve para uma base | **Reutilizável para Parceiro A, B, C...** sem alterar Python |

---

## 🎯 Problema Resolvido

**Cenário real:** Cada dia a operação roda 2–4 testes A/B diferentes. O time perde 2–4h só formatando planilhas antes mesmo de interpretar os resultados. 

**Soluução entregue:**
1. Operador **arrasta arquivo → clica "Iniciar"** 
2. Sistema: Lê CSV → Detecta schema automáticamente → Calcula métricas → Consulta IA Groq/Gemini/Ollama
3. Retorna: Decisão clara (**Grupo X escala por Y motivo**) + Relatório profissional (HTML) + Histórico consolidado (CSV)
4. Tempo total: **<30 segundos** vs **2 horas** manuais

---

## 🚀 Demonstração

### Fluxo visual da interface:

```
┌─────────────────────────────────────┐
│   MÉLIUZ - A/B TEST ANALYZER       │
├─────────────────────────────────────┤
│ Arquivo: [dataset_01_parceiroA.csv]│ ← Clique em Selecionar
│                                     │
┌─────────────────────────────────┐   │
│ RESUMO                          │   │
│ • Registro: 12,456              │   │
│ • Grupos: 3 (A, B, C)           │   │
│ • Balanceamento: OK             │   │
└─────────────────────────────────┘   │
│     [ Iniciar Análise]            │
│ ████████████████████░░░░ 100%       │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ STATUS                              │
│ ✔ Lendo arquivo CSV                │
✔ Calculando métricas...             │
✔ Consultando IA (Groq)...           │
✔ Gerando relatório...               │
✔ Salvando histórico...              │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ RESULTADO DA IA                     │
│                                     │
│  GRUPO RECOMENDADO: Grupo 3       │
│ NÍVEL DE CONFIANÇA: Alta            │
│                                     │
│ MOTIVOS:                            │
│ • Maior GMV (R$ 6.7M vs R$ 4.5M)    │
│ • Ticket médio mais saudável        │
│ • Cashback proporcional menor       │
│                                     │
│ RISCOS:                             │
│ • Diferença marginal em curto prazo │
│ ─────────────────────────────────── │
│ RESUMO ESTRATÉGICO:                 │
│ Escalar Grupo 3 gradualmente (20%   │
│ -> 50% -> 100%). Monitorar churn.   │
│                                     │
│ [📄 Abrir Relatório] [Limpar]       │
└─────────────────────────────────────┘
```

---

## Arquitetura

```
meliuz-ab-analyzer/
│
├── main.py                          # Entry point: cria App e roda Tkinter
│
├── src/                             # Módulos separados (SRP - Single Responsibility Principle)
│   ├── csv_reader.py                # Leitura robusta CSV (encoding, header detection, validação)
│   ├── analyzer.py                  # Motor de cálculo: sumariza métricas por grupo, detecta vencedor
│   ├── ai.py                        # Camada abstrata de IA:
│   ├── report.py                     # Gerador de relatórios (Markdown + HTML com CSS profissional)
│   ├── sheet.py                     # Historiador consolidado (CSV persistente entre execuções)
│   └── utils.py                     # Helpers auxiliares (opcional)
│
├── prompts/
│   └── prompt.md                   # ❗ ARQUIVO SEPARADO: instruções personalizadas da IA
│                                   # Modifique aqui sem tocar no código fonte!
│
├── reports/                         # SAÍDA DINÂMICA (gerada a cada análise):
│   ├── dataset_01_parceiroA.md      # Relatório técnico Markdown
│   ├── dataset_01_parceiroA.html     # Relatório visual para gestor
│   └── historico.csv                # Consolidado de todas análises realizadas
│
├── assets/
│   ├── datasets/
│   │   ├── dataset_01_parceiroA.csv # Entrada: teste A/B Parceiro A
│   │   ├── dataset_02_parceiroB.csv # Entrada: teste B/B Parceiro B
│   │   └── dataset_03_parceiroC.csv # Entrade: teste C/C Parceiro C
│   └── logo.png
│
├── .env                              # CONFIGURAÇÃO SENSÍVEL (está no ignore por conta da key)
├── requirements.txt                  # Dependências Python
├── LICENSE                           # Licença MIT
└── README.md                         # Este arquivo
```

## ✨ Funcionalidades Principais

### Para o Gestor (Visual)
- [x] **Interface gráfica intuitiva** (Tkinter responsivo, scroll automático)
- [x] **Relatório HTML** com cores semânticas (verde=vitória, laranja=risco)
- [x] **Botão one-click** "Abrir Relatório" abre HTML no navegador padrão
- [x] **Clear button** limpa tudo para nova análise

### Para o Analista (Técnico)
- [x] **Leitura automática de schemas** variados (detecta colunas pelo nome, não posição fixa)
- [x] **Validação de dados** (balanceamento <60%, amostra mínima, colunas obrigatórias)
- [x] **Fallback robusto** se IA falha (quota/erro): auto-analisa pelo GMV puro nunca trava a UI
- [x] **Multi-provedor/provider** suportado: Groq (gratis), Gemini, Ollama local

### Para a Arquitetura do Software
- [x] Cada módulo tem uma única responsabilidade
- [x] Novos dados/sem alterar código (via prompt.md e .csv externo)
- [x] Try/except global com tratamento específico por tipo de erro
- [x] Fácil adicionar novo provider (basta 15 linhas)

---

## 🛠️ Instalação Rápida

### Pré-requisitos
- Python >= 3.9 (testado até 3.13)
- Windows / Linux / macOS - Testado apenas em Windows
- Conexão internet (para IA na nuvem)
- API KEY da groq - gratuito - criar .env e colocar o que está no example
### Passo-a-passo

```bash
# 1. Clone/download do repo
git clone https://github.com/seu-usuario/meliuz-ab-analyzer.git
cd Resolucao_meliuz

# 2. Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install tkinter python-dotenv google-generativeai groq openpyxl

# 4. Configurar API de IA (escolha UM abaixo):

# Opção A: Groq (GRATUITO - Recomendado)
# Acesse https://console.groq.com/keys -> copie chave
echo "GROQ_API_KEY=gsk_sua_chave_aqui" > .env

# Opção B: Gemini (Google)
# Acesse https://aistudio.google.com/app/apikey
echo "GEMINI_API_KEY=AIzaSy..." >> .env

# 5. Customizar comportamento da IA (OPCIONAL)
echo "" > prompts/prompt.md
echo "Você é um growth hacker sênior..." >> prompts/prompt.md
# Edite-o conforme a linguagem da sua operação!

# 6. Executar
python main.py

# 7. Coloque arquivos CSV em assets/datasets/

# 8. Use! Arraste, clique Iniciar Análise.
```

**Importante:** O arquivo `.env` contém credenciais sensíveis. **Nunca commit no Git**. O `.gitignore` já deve conter `!.env`.

---

## 💻 Como Usar

### Uso Básico (3 cliques)

1. **Abrir aplicação:** `python main.py`
2. **Carregar dados:** Click *Selecionar* → Escolher `assets/datasets/dataset_01_parceiroA.csv`
3. **Executar:** Click *Iniciar Análise* → Aguarde ~15 segundos

**Saída gerada automaticamente:**
- ✅ `reports/dataset_01_parceiroA.html` (abrir no navegador)
- ✅ `reports/historico.csv` (linha adicionada com decisão)
- ✅ Caixa "Resultado da IA" preenchida com análise detalhada


#### Alterar critérios de decisão da IA

Edite `prompts/prompt.md`:
```
Atualmente pedimos JSON com {grupo_recomendado, confianca, motivos}
Você pode alterar para pedir ROI mínimo > X%,
ou considerar apenas testes com duração > 7 dias...
```
Salva arquivo e rode novamente. **Zero mudanças em Python**.

#### Adicionar novo dataset

Basta colocar novo `.csv` seguindo o schema:
```
Data;Grupos de usuários;Parceiro;compradores;comissão;cashback;vendas totais
2024-07-17;Grupo A;Meliuz;11410;"R$ 233.000";"R$ 503.600";"R$ 6785856"
```
O sistema detecta automaticamente colunas, calcula e decide.

#### Analisar múltiplos datasets seguidos?

Clique *Limpar* → Carregar próximo arquivo → *Iniciar Análise*. Cada resultado será registrado em `historico.csv`.

---

## 📊 Estrutura de Dados Esperados

O sistema aceita **qualquer CSV** que contenha estas palavras-chave nas colunas (case-insensitive):

| Campo Obrigatório | Palavras-chave aceitas | Exemplo de valor válido |
|---|---|---|
| Data/Teste | data, date, período | `2024-07-17` |
| Grupo/Variantes | grupo, variant, test group, grupo de usuários | `Grupo A`, `Controle` |
| Compradores | comprador, usuario, user, cliente, conversões | `11410`, `1234` |
| GMV/Vendas | gmv, receita, vendas totais, faturamento | `"R$ 6.785.856"` |
| Cashback | cashback, desconto, custo cashback | `"R$ 503.600"` |
| Comissão | comissão, custo operacional | `"R$ 98.200"` |
| Parceiro | parceiro, empresa, campanha | `Parceiro A` |

**Tolerâncias:**
- Ordem das colunas pode variar
- Caracteres especiais nos valores (R$, vírgulas) são removidos automaticamente
- Linhas vazias são ignoradas
- Encoding suportado: UTF-8, Latin-1 (ISO-8859-1), etc.

---

## 🔧 Customização

### Personalizar o comportamento da IA

O arquivo `prompts/prompt.md` controla **toda** a inteligência do sistema sem tocar em Python.

Exemplo de `prompt.md` avançado:
```
Você é um analista sênior de growth hacking especializado em cashback/afiliados.

REGRAS DE DECISÃO:
1. Só recomende escalar se Lift > 5% E p-value < 0.05
2. Nunca esquecer de mencionar riscos de churn
3. Priorize ticket médio bruto sobre taxa de conversão quando similar
4. Formato de resposta: JSON estrito com campos: grupo_recomendado, confianca, motivos[], riscos[], resumo

ESTILO:
- Use bullet points (-) para listas
- Máximo 250 palavras
- Seja direto ao ponto: "Escala Grupo A" (não "Eu recomendo...")
```

Ao salvar, próxima análise seguirá essas novas regras.

### Adicionar novo provider de IA

1. Em `src/ai.py`, dentro do `__init__()`:
```python
elif provider == "openai":
    from openai import OpenAI
    self.client = OpenAI(api_key=self.api_key)
    self.model_name = "gpt-4o-mini"
```

2. Chame assim:
```python
ai = AIAnalyzer(provider="openai")
```

**Total:** 15 linhas de código.

---

## 🔌 Integrações

### APIs Externas Suportadas

| Provider | Modelo | Custo | Quando usar | Configuração necessária |
|----------|--------|------|-------------|---------------------------|
| **Groq** | Llama 3.3 70B Versatile | **Gratuito** (alta quota) | Produção/Desenvolvimento diário | `GROQ_API_KEY=gsk_...` |
| **Gemini** | Gemini 1.5/2.0 Flash | **Gratuito** (limitado) | Testes rápidos, fallback | `GEMINI_API_KEY=AIza...` |
| **Ollama** | Qwen 2.5 / Llama 3 | **Local** (sem net) | Airgapped/offline | `provider="ollama"` |

### Geração de Saída

| Formato | Localização | Uso |
|---------|------------|-----|
| **HTML** (CSS profissional) | `reports/{nome}.html` | Visualização para gestão |
| **Markdown** (documentação) | `reports/{nome}.md` | Versionamento em Git |
| **CSV** (histórico) | `reports/historico.csv` | BI / PowerBI import |

---

## 📈 Métricas Monitoradas (O que o Sheet registra)

Por cada análise executada, o `historico.csv` captura:

```csv
Data;Parceiro;Grupo Recomendado;GMV;Cashback;Comissão;Ticket Médio;Relatório
"2025-07-17 14:32","Parceiro_A.csv","Grupo 3",6785856.00,503600.00,98200.00,594.73,"reports/Parceiro_A.md"
```

Estas informações podem ser importadas diretamente em:
- Google Sheets (Data > Connect to File > Upload)
- Power BI Desktop (Get Data > Text/CSV)
- Excel (Dados > Obter dados de texto/csv)

---

## 🐛 Solução de Problemas Comuns

### Problema: Interface aparece mas botão "Iniciar" não faz nada
**Causa:** Arquivo .env não configurado  
**Verificação:** Verificar logs no console/terminal  
**Resolução:** Confirmar `GROQ_API_KEY` ou `GEMINI_API_KEY` está definido no raiz opte pelo `GROQ_API_KEY` já validado é visivelmente mais veloz.

### Problema: "Usuários: 0" no resumo
**Causa:** Nome da coluna diferente ("Compradores" vs "usuarios")  
**Resolução:** Editar `src/analyzer.py`, linha onde busca "usuario" → adicionar "comprador"

### Problema: Erro 429/Quota exceeded
**Causa:** Limite gratuito da API atingido  
**Resolução:** 
1. Esperar 1 minuto (refresh) OU
2. Trocar provider (ex: Groq se Gemini cheio) OR
3. Usar `self.modelos[1]` como fallback (já implementado) 

### Problema: Relatório abre bagunçado no Excel
**Causa:** Separador CSV padrão `;` não reconhecido automaticamente  
**Resolução:** Ao abrir no Excel → Importar → Delimitador: `Ponto e vírgula` → Avançar

### Problema: AI responde texto solto ao invés de JSON
**Causa:** Modelo antigo ou fallback acionado  
**Resolução:** Verificar `logs` → Se mostrar "parse JSON failed" → Checar conexão internet / key válida

---

## 📝 Roadmap & Melhorias Futuras

### v1.0 - Current (Entregável) ✅
- [x] Interface funcional Tkinter
- [x] Leitura dinâmica de CSVs
- [x] Análise multi-provider (Groq/Gemini/Ollama)
- [x] Relatórios HTML + Markdown
- [ ] **Histórico consolidado**
- [x] Fallback automático (GMV puro se IA falhar)

### Melhorias futuras com tempo
- [ ] Dashboard comparativo lado a lado (Grupo A x B x C visualmente)
- [ ] Exportação em PDF (via weasyprint)
- [ ] Persistência SQLite para dashboard histórico longo-prazo
- [ ] Validação estatística automática (p-value, confidence interval, SRM detection)
- [ ] Sistema de alertas (slack/email) quando anomalia detectada
- [ ] Plug-in system: extensões de análise (clv, ltv, cohort retention)
- [ ] Scheduler: análisis automático todos os dias às 08:00
- [ ] Multi-language support (EN/ES/PT-BR automático baseado no locale do usuário)
- [ ] Streamlit wrapper versão web (para operações não-técnicas)

---

## 👥 Limitações Conhecidas

1. **Formato de entrada:** Atualmente exige CSV clássico. Futuras versões podem aceitar parquet/jsonl diretamente
2. **Escalabilidade de UI:** Tkinter processa tudo na thread principal. Para bases muito grandes (>100k linhas), recomendamos threading
3. **Validação Estatística:** Não implementa teste t-student ou Chi-square automaticamente. Recria puramente no GMV absoluto
4. **Persistência:** Histórico atual é CSV (append-only). Para produção enterprise, recomenda-se banco de dados
5. **Concorrência:** Se dois usuários usarem simultaneamente, podem haver escritas duplicadas no histórico (file lock recomendado)


---

## 📄 Licença

Este projeto é distribuído sob a licença MIT.

---

## 👨‍💻 Autor

**Italo Luan de Almeida**  
*Data:* Julho 2025  
*Stack do projeto:* Python 3.11+ / Tkinter / Groq AI  
*Status:* Disponível para estágio 

**Contato / Entrega:**
- Email: [contato.almeidagrupo@gmail.com]
- Portfolio: [www.linkedin.com/in/italo-almeida-966b42354]
- Repositório: [https://github.com/italozw/Resolucao_meliuz/tree/main]

---