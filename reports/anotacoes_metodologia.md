# Anotações da Metodologia — TCC Fraude Pix

Registro compartilhado de entendimentos importantes discutidos ao longo do cronograma.
Objetivo: virar base direta de parágrafos do TCC (principalmente Capítulo 3 — Metodologia) sem precisar reconstruir o raciocínio depois. Preencher juntos (Letícia e Lucas) conforme as tarefas do [cronograma](https://letalves.github.io/tcc-fraude-cartao/) forem concluídas.

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

<!-- Próxima entrada: tarefas m1_p1_0c/0d (grupos de colunas C/D/M/V, features de identidade id_01-id_38) -->
