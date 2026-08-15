# Anotações da Metodologia — TCC Fraude Pix

Registro compartilhado de entendimentos importantes discutidos ao longo do cronograma.
Objetivo: virar base direta de parágrafos do TCC (principalmente Capítulo 3 — Metodologia) sem precisar reconstruir o raciocínio depois. Preencher juntos (Letícia e Lucas) conforme as tarefas do [cronograma](https://letalves.github.io/tcc-fraude-cartao/) forem concluídas.

---

## Maio — Fundação do projeto

### Tarefa: Ler a proposta e entender a metodologia (m1_p1_0a)

- **SHAP explica o quê**: aponta quais variáveis da transação mais influenciaram a decisão do modelo. É a explicação técnica, específica de cada transação.
- **RAG contextualiza com fontes**: recupera trechos regulatórios, científicos e setoriais relacionados a conceitos com semântica validada e os fornece ao LLM para redigir uma explicação rastreável. O RAG não descobre o significado de uma coluna anônima.
- **Frase-chave para o Capítulo 3**: SHAP = *o que influenciou o modelo*; RAG = *qual contexto documental verificável ajuda a interpretar a evidência*. A ponte exige um registro de atributos semânticos; nomes anônimos como `V258` não devem virar consultas Pix por suposição.

### Tarefa: Estudar o contexto Pix — golpes típicos (m1_p1_0e)

- **Golpe do falso funcionário**: fraudador se passa por atendente do banco e convence a vítima a fazer o Pix ou a passar a senha/código. A vítima pode iniciar a transação sob manipulação. O Pix não possui chargeback automático equivalente ao cartão; casos de fundada suspeita de fraude podem seguir o **MED (Mecanismo Especial de Devolução)**, introduzido pela Resolução BCB nº 103/2021. Procedimentos e prazos devem ser citados a partir do Regulamento do Pix e do Guia do MED vigentes na data analisada.
- **Engenharia social (categoria ampla)**: inclui golpe do parente/emergência, falso vendedor/comprador, QR Code adulterado e falsas promoções ou investimentos. Esses cenários motivam atributos comportamentais explícitos, como desvio de valor e frequência recente. Os grupos `C*` e `D*` podem carregar sinais estatísticos, mas seu significado individual não foi divulgado e não prova um tipo de golpe.
- **Clonagem de dados/conta**: envolve acesso não autorizado, por exemplo após phishing, malware ou comprometimento de credenciais. `DeviceType` e `DeviceInfo` podem apoiar uma análise de contexto do dispositivo quando presentes; não é válido afirmar que cada `id_*` ou `M*` mede dispositivo novo, conta antiga ou identidade Pix.

**Por que importa pro TCC**: orienta hipóteses para atributos comportamentais e a seleção do corpus. Os documentos do BCB sustentam regras e procedimentos; o relatório FEBRABAN fornece contexto setorial. Nenhum deles valida sozinho a correspondência entre uma coluna anônima do IEEE-CIS e um padrão Pix.

### Tarefa: Entender as duas tabelas do dataset IEEE-CIS (m1_p1_0b)

- **`train_transaction.csv`** — 394 colunas, ~590k linhas. Uma linha = uma transação. Principais: `TransactionID` (chave), `isFraud` (alvo, 0/1 — fortemente desbalanceado, ~3,5% fraude), `TransactionDT` (segundos desde um ponto de referência arbitrário, não é data real), `TransactionAmt`, `ProductCD`, `card1-card6` (dados do cartão mascarados), grupos `C1-C14`/`D1-D15`/`M1-M9`/`V1-V339`.
- **`train_identity.csv`** — 41 colunas, bem menor (nem toda transação tem linha de identidade). Chave `TransactionID` faz o *left join* com a tabela principal. Colunas: `id_01-id_38` (anônimas, rede/dispositivo), `DeviceType` (mobile/desktop), `DeviceInfo` (modelo/SO — confirmado no preview: pode vir `NaN` mesmo com `DeviceType` preenchido, ou seja, dado incompleto é esperado e precisa ser tratado no pré-processamento).
- Preview real rodado localmente confirmou a estrutura: linhas de `train_transaction` majoritariamente `isFraud=0`; join por `TransactionID` funciona como esperado entre as duas tabelas.

### Tarefa: Estudar os grupos de colunas C/D/M/V (m1_p1_0c)

Contagem real confirmada no `train_transaction.csv`: **C1–C14** (14 colunas), **D1–D15** (15), **M1–M9** (9), **V1–V339** (339 — ~86% de todas as 394 colunas). Todas anonimizadas de propósito pela Vesta, sem dicionário oficial — só a categoria geral é conhecida:

- **C1–C14 (contagens)**: a categoria geral é de contagens. O evento contado por cada coluna não foi publicado; exemplos encontrados na comunidade são hipóteses, não dicionário oficial.
- **D1–D15 (deltas de tempo)**: a categoria geral é de deltas temporais. Não é seguro atribuir a cada coluna um evento como "abertura da conta" sem fonte.
- **M1–M9 (matches)**: indicadores de correspondência do domínio original, com significado individual não divulgado. Não equivalem automaticamente a conferências de identidade Pix.
- **V1–V339 (features Vesta)**: atributos numéricos engenheirados e anonimizados. O modelo e o SHAP indicam influência estatística, mas não recuperam o significado oculto nem estabelecem causalidade.

**Por que importa pro TCC**: sem significado semântico, o pré-processamento deve ser estatístico e documentado. O SHAP mostra quais colunas pesaram na decisão; a explicação em linguagem natural só pode usar conceitos definidos por atributos explícitos ou derivados validados.

### Revisão da Pessoa 2 — correções e ponte SHAP → RAG (m1_p2_0a–0d)

- O MED foi introduzido pela **Resolução BCB nº 103/2021**. A Resolução nº 403 é de 22/07/2024 e não criou o mecanismo.
- No treino local, `train_identity.csv` cobre **144.233 de 590.540 transações (24,4%)**, e não aproximadamente 60%.
- O IEEE-CIS é um dataset de comércio eletrônico/cartão usado como proxy técnico; resultados não comprovam desempenho em Pix real.
- A investigação, referências e regras para o corpus estão em `reports/pessoa_2/maio/`.

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
