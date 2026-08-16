# Anotações da Metodologia — TCC Fraude Pix

Registro compartilhado de entendimentos importantes discutidos ao longo do cronograma.
Objetivo: virar base direta de parágrafos do TCC (principalmente Capítulo 3 — Metodologia) sem precisar reconstruir o raciocínio depois. Preencher juntos (Letícia e Lucas) conforme as tarefas do [cronograma](https://letalves.github.io/tcc-fraude-pix/) forem concluídas.

---

## Maio — Fundação do projeto

### Tarefa: Ler a proposta e entender a metodologia (m1_p1_0a)

- **SHAP explica o quê**: aponta quais variáveis da transação mais influenciaram a decisão do modelo. É a explicação técnica, específica de cada transação.
- **RAG explica o que isso significa**: busca documentos regulatórios (BACEN, FEBRABAN) e descrições de padrões de fraude compatíveis com o que o SHAP apontou, e gera a explicação em linguagem natural para o usuário/analista.
- **Frase-chave para o Capítulo 3**: SHAP = *o quê* (quais variáveis pesaram); RAG = *o que isso significa* (contexto regulatório/humano). Sem o SHAP, o RAG não sabe o que buscar — as duas camadas são complementares, não substitutas.

### Tarefa: Estudar o contexto Pix — golpes típicos (m1_p1_0e)

- **Golpe do falso funcionário**: fraudador se passa por atendente do banco e convence a vítima a fazer o Pix ou a passar a senha/código. A vítima autoriza a transação por conta própria — não é invasão, é manipulação. Por isso o Pix não tem chargeback automático como o cartão; a devolução só ocorre via **MED (Mecanismo Especial de Devolução)**, criado pela Resolução BCB nº 403/2023, e depende de ação rápida da instituição (~80h após o alerta).
- **Engenharia social (categoria ampla)**: inclui golpe do parente/emergência (WhatsApp clonado), falso vendedor/comprador em marketplace, QR Code falso substituído, falsas promoções/investimentos. Característica comum: os dados/dispositivo da vítima continuam sendo dela — o que muda é o *comportamento* (transação fora do padrão, destinatário novo, horário incomum). Colunas `D1-D15` (tempo desde última transação) e `C1-C14` (contagens) tentam capturar esse tipo de sinal.
- **Clonagem de dados/conta**: acesso não autorizado (phishing, malware, SIM swap) — a transação acontece *sem* o conhecimento da vítima, direto pelo app dela. É o cenário de "dispositivo desconhecido logando numa conta antiga", capturado pelas colunas de identidade (`DeviceType`, `DeviceInfo`, `id_01-id_38`) e `M1-M9` (flags de correspondência entre dispositivo/conta).

**Por que importa pro TCC**: base para a engenharia de features Pix de junho (`dispositivo_novo`, `hora_suspeita`, `valor_atipico`) e para a base de conhecimento do RAG de julho (Resolução BCB 403/2023, relatório FEBRABAN descrevem exatamente esses padrões).

### Tarefa: Entender as duas tabelas do dataset IEEE-CIS (m1_p1_0b)

- **`train_transaction.csv`** — 394 colunas, ~590k linhas. Uma linha = uma transação. Principais: `TransactionID` (chave), `isFraud` (alvo, 0/1 — fortemente desbalanceado, ~3,5% fraude), `TransactionDT` (segundos desde um ponto de referência arbitrário, não é data real), `TransactionAmt`, `ProductCD`, `card1-card6` (dados do cartão mascarados), grupos `C1-C14`/`D1-D15`/`M1-M9`/`V1-V339`.
- **`train_identity.csv`** — 41 colunas, bem menor (nem toda transação tem linha de identidade). Chave `TransactionID` faz o *left join* com a tabela principal. Colunas: `id_01-id_38` (anônimas, rede/dispositivo), `DeviceType` (mobile/desktop), `DeviceInfo` (modelo/SO — confirmado no preview: pode vir `NaN` mesmo com `DeviceType` preenchido, ou seja, dado incompleto é esperado e precisa ser tratado no pré-processamento).
- Preview real rodado localmente confirmou a estrutura: linhas de `train_transaction` majoritariamente `isFraud=0`; join por `TransactionID` funciona como esperado entre as duas tabelas.

### Tarefa: Estudar os grupos de colunas C/D/M/V (m1_p1_0c)

Contagem real confirmada no `train_transaction.csv`: **C1–C14** (14 colunas), **D1–D15** (15), **M1–M9** (9), **V1–V339** (339 — ~86% de todas as 394 colunas). Todas anonimizadas de propósito pela Vesta, sem dicionário oficial — só a categoria geral é conhecida:

- **C1–C14 (contagens)**: ex. quantos endereços/e-mails diferentes associados ao cartão. Sinaliza comportamento "espalhado", comum em fraude (cartão roubado usado em vários lugares).
- **D1–D15 (deltas de tempo)**: dias entre eventos (última transação, abertura da conta). Captura frequência/recência — golpes tendem a fugir do ritmo normal do usuário.
- **M1–M9 (matches T/F)**: ex. nome do titular bate com nome de cobrança, endereço bate com o do cartão. Sinaliza inconsistência de identidade, ligado a clonagem/conta comprometida.
- **V1–V339 (features Vesta)**: engenharia própria da Vesta, numéricas, sem nome nem explicação — "caixa-preta". Só o modelo + SHAP conseguem apontar quais pesam na decisão.

**Por que importa pro TCC**: sem significado semântico, o pré-processamento (junho) precisa ser estatístico (nulos por grupo, correlação entre V's pra reduzir redundância) — e é o SHAP que depois "traduz" quais colunas anônimas pesaram em cada decisão.

### Tarefa: Entender as features de identidade (m1_p1_0d)

- **`id_01` a `id_11`**: numéricas, ligadas à conexão de rede (score de risco de IP, proxy/VPN, sinal digital do dispositivo).
- **`id_12` a `id_38`**: categóricas — flags "Found"/"NotFound", tipo de navegador, resolução de tela, correspondência entre dispositivo salvo e o usado na transação.
- **`DeviceType`**: mobile ou desktop.
- **`DeviceInfo`**: texto livre (modelo/SO), alta cardinalidade — precisa de limpeza/agrupamento antes de virar feature categórica.

**Números reais do `train_identity.csv`** (144.233 linhas):
- `DeviceType`: 85.165 desktop / 55.645 mobile / 3.423 nulos (~2,4% — coluna confiável).
- `DeviceInfo`: 1.786 valores distintos; top 5 = Windows (47.722), nulo (25.567 = ~17,7%), iOS Device (19.782), MacOS (12.573), Trident/7.0 = IE11 (7.440).
- Das 38 colunas `id_`, a taxa de nulos varia muito: `id_01` tem 0% nulo, mas `id_07`/`id_08` têm **96,4% de nulos** — praticamente inúteis como estão.

**Por que importa pro TCC**: colunas `id_` com nulo acima de ~90% (ex: id_07/id_08) devem ser descartadas ou viram só uma flag binária "tem dado ou não" no pré-processamento, em vez de imputação — decisão que só foi possível ver rodando os dados reais, não só lendo a documentação do Kaggle.

<!-- Próxima entrada: tarefa m1_p1_3 (rodar 01_eda.ipynb) e m1_p1_4 (documentar achados em reports/eda_summary.txt) -->
