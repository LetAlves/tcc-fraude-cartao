# Recomendação de LLM para a camada de geração

Data da análise: **30/08/2026**. Escopo: preparação de `m3_ab_1`.

## Objetivo

Comparar as duas alternativas previstas no cronograma — Claude API e Llama local via Ollama — e propor uma decisão que a dupla possa validar. Nenhuma chave foi configurada e nenhuma informação foi enviada a um LLM nesta etapa.

## Recomendação

**Usar Claude Haiku 4.5 como opção principal do protótipo e manter Ollama como alternativa local de privacidade e contingência.** A tarefa conjunta permanece pendente até Letícia e Lucas aprovarem a escolha, a política de dados e um teto de custo.

| Critério | Claude Haiku 4.5 | Llama local via Ollama |
|---|---|---|
| Implantação inicial | API simples; exige chave e internet | exige instalação, armazenamento e hardware compatível |
| Privacidade | dados saem do computador; exige minimização | processamento pode permanecer local |
| Reprodutibilidade | fixar ID do modelo, prompt e parâmetros | fixar modelo, quantização, versão do Ollama e hardware |
| Custo | variável por tokens | sem custo por token, mas usa máquina e energia |
| Operação no computador atual | não depende de GPU local | ainda requer auditoria de RAM/VRAM e latência |
| Papel recomendado | geração principal da demonstração | fallback e comparação experimental, se viável |

A [página oficial do Claude Haiku 4.5](https://www.anthropic.com/claude/haiku) informa o identificador `claude-haiku-4-5` e preços públicos por tokens. No lado local, o [Ollama lista o Llama 3](https://ollama.com/blog/llama3) nas variantes históricas 8B e 70B; o [Llama 3.3 atual no catálogo](https://ollama.com/library/llama3.3%3Alatest) é um modelo 70B e seu artefato quantizado principal é grande. A [documentação de contexto do Ollama](https://docs.ollama.com/context-length) alerta que ampliar o contexto aumenta o uso de memória.

## Política mínima para a API

Se Claude for aprovado:

1. enviar somente transações sintéticas ou atributos minimizados;
2. não enviar token Kaggle, chaves de API, nomes, e-mails ou identificadores reais;
3. limitar o contexto aos chunks recuperados e ao pacote SHAP necessário;
4. registrar ID do modelo, versão do prompt, temperatura, IDs dos chunks e data;
5. aplicar timeout, tentativas limitadas e tratamento de indisponibilidade;
6. impor teto mensal de custo e limite de tokens por requisição;
7. separar a saída do LLM da decisão do classificador e impedir ações automáticas.

## Critérios para a decisão conjunta

- [x] Letícia e Lucas aprovam Claude Haiku 4.5 como modelo principal ou escolhem a alternativa local — **aprovado em 30/08/2026** (Claude Haiku 4.5 principal + Ollama fallback), ver `reports/reunioes/2026-08-30_kickoff.md`. Confirmação do Lucas ainda pendente de registro.
- [ ] A dupla aprova que apenas dados sintéticos/minimizados podem sair do ambiente local.
- [ ] Define-se um teto de custo mensal e quem administra a chave.
- [ ] Se Ollama for exigido, registra-se RAM, VRAM, modelo, quantização e latência no computador de demonstração.
- [ ] Um conjunto fixo de perguntas compara suporte documental, coerência com SHAP, abstenção e tempo de resposta.

O modelo em si está aprovado; os sub-itens operacionais acima (política de dados, custo, chave, hardware, perguntas de comparação) ainda estão em aberto.
