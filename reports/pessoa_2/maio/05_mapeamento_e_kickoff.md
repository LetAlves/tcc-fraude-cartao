# Mapeamento IEEE-CIS -> Pix e preparação do kickoff

## 1. Evidência da leitura do dicionário

Foi feita extração estrutural completa de `reports/dicionario_dados.docx` e cruzamento com os CSVs locais. A auditoria encontrou significados individuais sem fonte e uma cobertura de identidade incorreta. O gerador `scripts/gerar_dicionario.py` foi corrigido e o DOCX foi regenerado com descrições no nível de evidência realmente publicado.

A validação estrutural do novo arquivo confirmou 11 tabelas, 38 linhas de tabela, presença dos grupos obrigatórios, ausência das afirmações antigas e integridade do pacote DOCX. A renderização visual não pôde ser executada porque o LibreOffice/`soffice` não está instalado; portanto, o conteúdo foi validado, mas a diagramação final ainda deve ser inspecionada no Word ou LibreOffice.

Estatísticas reproduzidas diretamente dos dados de treino:

| Medida | Valor |
|---|---:|
| transações em `train_transaction.csv` | 590.540 |
| fraudes marcadas | 20.663 |
| proporção `isFraud = 1` | 3,499% |
| linhas em `train_identity.csv` | 144.233 |
| cobertura de identidade após `left join` | 24,424% |

Logo, a afirmação de que os dados de identidade aparecem em aproximadamente 60% das transações foi corrigida: no treino local, a cobertura é cerca de **24,4%**.

## 2. Auditoria de afirmações do dicionário

Os itens abaixo registram o critério aplicado na correção do documento, para impedir que uma edição futura reintroduza inferências como fatos.

### Pode ser afirmado

- `TransactionID` liga as tabelas de transação e identidade;
- `isFraud` é o alvo do treino;
- `TransactionDT` representa um delta em segundos a partir de uma referência não publicada;
- `TransactionAmt` é o valor da transação;
- `DeviceType` e `DeviceInfo` têm significado direto, embora incompletos;
- a descrição oficial fornece significado por grupos para parte das colunas.

### Exige cautela ou correção

- significados individuais detalhados para `C1-C14`, `D1-D15`, `M1-M9`, `V1-V339` e `id_01-id_38` não estão documentados oficialmente;
- exemplos comunitários não devem ser apresentados como dicionário factual;
- não há base para afirmar que `D1` é universalmente a variável mais importante antes dos experimentos;
- `TransactionDT` não deve ser convertido em data civil real; `mod 86400` produz uma posição cíclica relativa, não "hora local do Pix";
- `isFraud` no IEEE-CIS não equivale a uma decisão de MED;
- `ProductCD`, cartões, e-mails e endereços descrevem o domínio original e não devem ser renomeados como conta/chave/destinatário Pix.

## 3. Mapeamento aceitável: papel analítico, não equivalência semântica

| Dado IEEE-CIS | Papel analítico na prova de conceito | Limite no contexto Pix |
|---|---|---|
| `TransactionAmt` | magnitude e desvio de valor | moeda e comportamento do usuário Pix não são confirmados |
| `TransactionDT` | ordem, recência e janelas relativas | origem temporal e fuso são desconhecidos |
| `card*` | identificador mascarado para agregações de histórico | não representa chave ou conta Pix |
| `addr*`, `P_emaildomain`, `R_emaildomain` | sinais contextuais do comércio eletrônico | não representam necessariamente pagador/recebedor Pix |
| `DeviceType`, `DeviceInfo` | contexto de dispositivo quando presente | cobertura de identidade é ~24,4% no treino |
| `C*`, `D*`, `M*`, `V*`, `id_*` | atributos estatísticos/anônimos para o classificador | sem tradução individual para conceitos Pix |

A redação adequada é: **"atributo com papel analítico análogo"**, seguida da limitação. A redação inadequada é: **"C1 mede contas Pix do destinatário"**.

## 4. Registro proposto para atributos explicáveis

Os atributos derivados precisam ser implementados e validados antes de serem usados no RAG.

| ID semântico proposto | Definição possível no IEEE-CIS | Tag RAG | Advertência |
|---|---|---|---|
| `valor_atipico_proxy` | desvio robusto de `TransactionAmt` no histórico anterior do mesmo `card1`, calculado dentro da partição | `valor_atipico` | `card1` é proxy, não conta Pix |
| `frequencia_recente_proxy` | contagem anterior em janela relativa de `TransactionDT` para `card1` | `frequencia_incomum` | evitar usar eventos futuros |
| `dispositivo_raro_proxy` | raridade de `DeviceInfo` no histórico anterior do proxy | `dispositivo_incomum` | disponível apenas onde há identidade |
| `posicao_ciclo_diario_relativa` | componente cíclico de `TransactionDT mod 86400` | `padrao_temporal` | não chamar de horário local |

Requisitos do registro definitivo: fórmula, colunas-fonte, população, janela, unidade, tratamento de nulos, risco de vazamento, autor, versão e testes. Até isso existir, o RAG não deve consultar por essas tags.

## 5. Proposta de decisões para o kickoff

Estas são recomendações técnicas, ainda não uma ata aprovada pela dupla.

### Responsabilidades

| Área | Responsável primário | Revisão cruzada |
|---|---|---|
| dados, modelos e SHAP | Letícia / Pessoa 1 | Lucas valida documentação e limites |
| corpus, RAG e texto | Lucas / Pessoa 2 | Letícia valida coerência com o modelo |
| integração e avaliação | ambos | aprovação do orientador nos marcos |

### Ferramentas recomendadas

- GitHub com branch por entrega e pull request para `main`;
- projeto LaTeX versionado e, após decisão da dupla, importado no Overleaf;
- Zotero compartilhado opcional; o `.bib` do repositório continua como artefato reproduzível;
- `sentence-transformers` para embeddings e FAISS local para o protótipo;
- adaptador de LLM configurável por variável de ambiente, sem chave no Git;
- planilha ou Markdown de experimentos com versão do código, dados, seed, parâmetros e métricas.

### Decisões que a dupla precisa tomar

- [x] data e frequência da reunião semanal — **domingo, 19h** (ver `reports/reunioes/2026-08-30_kickoff.md`);
- [x] Overleaf ou Google Docs como ambiente editorial oficial — **Overleaf confirmado**;
- [x] quem cria e compartilha a conta/projeto externo — **Letícia cria e convida o Lucas**;
- [x] modelo de embeddings após teste em português — **aprovado**, `src/rag/embeddings.py`;
- [x] LLM remoto ou local, considerando custo, privacidade e reprodutibilidade — **aprovado**: Claude Haiku 4.5 principal + Ollama fallback (sub-itens operacionais ainda pendentes, ver `reports/pessoa_2/julho/03_decisao_llm.md`);
- [x] protocolo de revisão de fontes e atualização de normas — **aprovado**, ver `reports/reunioes/2026-08-30_kickoff.md`;
- [ ] data dos marcos internos antes das entregas ao orientador (sem data definida — lembrete);
- [ ] manual/template institucional de TCC (sem data definida — lembrete).

## 6. Modelo de ata a preencher

```text
Data:
Participantes:

Decisões:
1.
2.
3.

Responsáveis e prazos:
- Letícia:
- Lucas:
- Ambos:

Bloqueios:

Próxima reunião:
```

## 7. Critério para concluir as tarefas conjuntas

Após a conversa, a dupla deve acrescentar a ata neste arquivo ou em `reports/reunioes/`, registrar as decisões e abrir um pull request. **Kickoff concluído em 30/08/2026** — ata em `reports/reunioes/2026-08-30_kickoff.md`. Confirmação do Lucas sobre os itens ainda pendente de registro.
