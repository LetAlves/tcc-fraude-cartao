# TCC — Fraude Pix com Machine Learning, SHAP e RAG

Prova de conceito acadêmica para **detecção e explicação de risco de fraude em contexto Pix**, combinando classificação por aprendizado de máquina, explicações locais com SHAP e recuperação de fontes documentais com RAG.

**Autores:** Letícia Alves — Pessoa 1 (ML e dados); Lucas Nogueira — Pessoa 2 (RAG e escrita).

> O IEEE-CIS contém transações do domínio de comércio eletrônico/cartão, não transações Pix reais. As features do projeto representam analogias analíticas documentadas. Os experimentos não comprovam desempenho operacional no Pix e o protótipo não deve ser usado para bloquear transações ou acusar pessoas.

[Guia do TCC](https://letalves.github.io/tcc-fraude-pix/) · [Entregas de maio](reports/pessoa_2/maio/README.md) · [Entregas de junho](reports/pessoa_2/junho/README.md) · [Monografia](monografia/README.md) · [Como contribuir](CONTRIBUTING.md)

## Arquitetura proposta

```text
Dados IEEE-CIS + features proxy documentadas
  → pré-processamento e classificação de risco (ML)
  → contribuições locais dos atributos (SHAP)
  → recuperação de fontes e explicação com citações (RAG + LLM)
```

O classificador estima risco; SHAP descreve a influência dos atributos; o RAG fornece contexto documental. Uma contribuição SHAP não prova causalidade e uma coluna anônima não ganha significado Pix por ser importante para o modelo.

O [registro de features](config/pix_feature_registry.json) descreve os conceitos controlados que podem alimentar a futura ponte SHAP → RAG.

## Estado do projeto

Situação verificada nesta versão em **27/08/2026**. Dependências instaladas não significam que todas as camadas já estejam implementadas.

| Componente | Situação | Evidência |
|---|---|---|
| Download, leitura e junção dos dados | Implementados | [Data loader](src/data_loader.py) |
| Análise exploratória | Notebook executado | [EDA](notebooks/01_eda.ipynb) |
| Features Pix simuladas | Quatro conceitos implementados, gerando seis colunas | [Módulo de features](src/features/pix_features.py) e [ata de aprovação](reports/reunioes/2026-08-16_mapeamento_ieee_cis_pix.md) |
| Estudo de LangChain | Laboratório local com retriever lexical e prompt; sem chamada a LLM | [Guia prático](reports/pessoa_2/junho/01_estudo_langchain.md) |
| Monografia | Rascunhos dos Capítulos 1, 2 e 3 e bibliografia BibTeX | [Projeto de escrita](monografia/README.md) |
| Pré-processamento, SMOTE e primeiros modelos | Pendentes de implementação e avaliação | [Protocolo metodológico](reports/pessoa_2/junho/03_metodologia_tres_camadas.md) |
| SHAP integrado, RAG vetorial e interface de demonstração | Planejados | [Arquitetura e RAG](reports/pessoa_2/maio/01_guia_arquitetura_e_rag.md) |

O laboratório de LangChain não é o RAG final. Os textos da monografia ainda exigem revisão da dupla e do orientador; um relatório preparado não comprova seu envio ao orientador.

## Instalação — Windows / PowerShell

Pré-requisitos: Git e Python. O ambiente de desenvolvimento foi validado com **Python 3.12**.

```powershell
git clone https://github.com/LetAlves/tcc-fraude-pix.git
cd tcc-fraude-pix
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Execute os comandos seguintes na raiz do repositório. Eles usam diretamente o Python da venv, sem exigir sua ativação ou alteração da política de execução do PowerShell. Em Linux/macOS, o executável equivalente é `.venv/bin/python`.

As dependências estão em [requirements.txt](requirements.txt). Atualmente elas usam limites mínimos de versão, sem um lockfile; registre as versões efetivamente utilizadas em cada experimento.

## Dataset e autenticação Kaggle

1. Acesse a competição [IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection) e aceite suas [regras](https://www.kaggle.com/competitions/ieee-fraud-detection/rules) na própria conta. O acesso pode exigir verificações adicionais do Kaggle.
2. Gere seu token na seção API das configurações do Kaggle.
3. Salve somente o valor do token em `%USERPROFILE%\.kaggle\access_token`, fora deste repositório. Como alternativa, configure `KAGGLE_API_TOKEN` no arquivo local `.env`.
4. Baixe e extraia os dados:

```powershell
.\.venv\Scripts\python.exe -c "from src.data_loader import _baixar_kaggle; _baixar_kaggle()"
```

Para os módulos atuais, os arquivos necessários são:

```text
data/raw/
├── train_transaction.csv
└── train_identity.csv
```

O download da competição também pode trazer outros CSVs. Se os dois arquivos de treino já existirem, `carregar_dados()` os reutiliza sem baixar novamente.

### Dados e segredos não vão para o Git

- O [.gitignore](.gitignore) exclui `data/raw/`, `data/processed/`, `.venv/` e `.env`.
- Não faça commit dos CSVs, de tokens ou de credenciais; não use `git add -f` para contornar essas exclusões.
- Cada integrante pode obter os dados com sua própria conta Kaggle. Google Drive e DVC **não estão configurados** neste projeto; qualquer compartilhamento externo deve respeitar as regras da fonte.
- Código, testes, documentação e estatísticas agregadas podem ser versionados sem incluir o dataset bruto.

Para verificar localmente:

```powershell
git check-ignore data/raw/train_transaction.csv data/processed/exemplo.csv .env
git ls-files data
```

O segundo comando deve retornar vazio. O `.gitignore` não remove arquivos que já tenham sido rastreados; revise sempre `git diff --cached` antes de fazer commit.

## Como executar

### Verificar a leitura dos dados

```powershell
.\.venv\Scripts\python.exe -m src.data_loader
```

Esse teste lê até 1.000 linhas de cada tabela e faz a junção por `TransactionID`. Se os arquivos estiverem ausentes, tentará baixá-los usando a configuração Kaggle.

### Abrir a análise exploratória

```powershell
.\.venv\Scripts\python.exe -m jupyter notebook notebooks/01_eda.ipynb
```

A EDA completa exige mais memória que os testes com amostras. Execute as células em ordem e preserve as limitações de interpretação dos atributos anonimizados.

### Executar as features Pix simuladas

```powershell
.\.venv\Scripts\python.exe -m src.features.pix_features
```

O teste usa até 50.000 linhas de cada tabela, calcula as features e imprime um resumo. Ele não treina modelos nem grava automaticamente um novo dataset.

Os quatro conceitos são `valor_atipico_cartao_proxy`, `frequencia_recente_cartao_proxy`, `dispositivo_raro_cartao_proxy` e `posicao_ciclo_diario_relativa`. O último inclui também codificações seno e cosseno. `card1` não é uma conta Pix, e o ciclo temporal não representa um horário local conhecido.

### Executar o laboratório de LangChain

```powershell
.\.venv\Scripts\python.exe -m src.rag.langchain_basics
```

Não exige dataset, download de embeddings ou chave de LLM. Recupera documentos didáticos e imprime o prompt montado; não gera uma resposta com modelo de linguagem.

### Reproduzir o relatório de junho

```powershell
.\.venv\Scripts\python.exe scripts/gerar_entrega_junho.py
```

Lê colunas selecionadas dos CSVs completos e **atualiza** [a entrega parcial de EDA e features](reports/pessoa_2/junho/04_entrega_parcial_eda_features.md). Para preservar o relatório versionado e gerar uma cópia local:

```powershell
.\.venv\Scripts\python.exe scripts/gerar_entrega_junho.py --output data/processed/entrega_junho.md
```

## Testes e protocolo experimental

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
git diff --check
```

Os testes atuais cobrem o laboratório LangChain, o registro de features, estatísticas em dados sintéticos e referências dos capítulos. Eles não medem desempenho preditivo nem substituem uma validação completa das features e dos modelos.

Para os próximos experimentos:

- separar treino, validação e teste antes de ajustar transformações;
- aplicar SMOTE somente no treino de cada partição ou fold;
- calcular atributos históricos sem usar eventos futuros;
- selecionar o limiar na validação e preservar o teste para avaliação final;
- registrar seed, versões, parâmetros, features e métricas da classe rara, incluindo AUC-PR, precisão, recall e F1;
- não apresentar métricas ainda não obtidas em experimentos executados.

## Organização do repositório

```text
config/                  Registro semântico das features proxy
data/raw/                CSVs originais locais — ignorados pelo Git
data/processed/          Dados derivados locais — ignorados pelo Git
docs/                    Guia e cronograma estático do TCC
monografia/              LaTeX, capítulos e bibliografia BibTeX
notebooks/               Análise exploratória
reports/                 Entregas, dicionário, anotações e atas
scripts/                 Geração de documentos e relatórios
src/data_loader.py       Download, leitura e junção dos dados
src/features/            Engenharia de features Pix simuladas
src/models/              Estrutura reservada para os modelos
src/rag/                 Laboratório e evolução do RAG
tests/                   Testes automatizados
```

O organizador colaborativo de tarefas é um projeto separado; este repositório reúne os artefatos acadêmicos e o código do TCC.

## Monografia e contribuição

A entrada LaTeX é [monografia/main.tex](monografia/main.tex), com fontes em [referencias.bib](monografia/referencias.bib). Siga o [guia do Overleaf](monografia/README.md), confirme o template da instituição e compile os capítulos antes da entrega final.

Trabalhe em branches, faça commits focados e peça revisão da outra pessoa antes de integrar à `main`. As convenções e os critérios de revisão estão em [CONTRIBUTING.md](CONTRIBUTING.md).
