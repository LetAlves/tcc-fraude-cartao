# Revisão de artigos e referências bibliográficas

## 1. Estratégia da busca

Consultas-base do cronograma: `Pix fraud detection`, `financial fraud machine learning`, `credit card fraud detection class imbalance` e `fraud detection concept drift`. Foram priorizados artigos revisados por pares, páginas oficiais dos periódicos, DOI e versões institucionais abertas. A busca por "Pix fraud detection" retorna literatura ainda heterogênea; por isso, a base teórica principal usa estudos consolidados de fraude transacional e explicita a diferença de domínio.

Critérios de inclusão:

- problema de fraude financeira ou classificação rara;
- método e avaliação descritos;
- contribuição aplicável ao desenho experimental;
- metadados verificáveis em editora, DOI ou repositório institucional.

## 2. Quatro artigos lidos

### 2.1 Abdallah, Maarof e Zainal (2016) - visão geral do campo

**Artigo:** [Fraud detection system: A survey](https://doi.org/10.1016/j.jnca.2016.04.007), *Journal of Network and Computer Applications*, 68, 90-113.

O survey organiza técnicas de detecção e destaca dificuldades recorrentes: forte desbalanceamento, mudança dos padrões ao longo do tempo, grande volume e necessidade de resposta rápida. A contribuição para o TCC é evitar tratar fraude como uma classificação estática comum.

**Aplicação:** justificar métricas para classe rara, validação temporal quando possível e monitoramento de mudança de distribuição.

**Limite:** é uma síntese anterior ao Pix e não valida diretamente o dataset IEEE-CIS nem o contexto regulatório brasileiro.

### 2.2 Jurgovsky et al. (2018) - comportamento sequencial

**Artigo:** [Sequence classification for credit-card fraud detection](https://doi.org/10.1016/j.eswa.2018.01.037), *Expert Systems with Applications*, 100, 234-245.

O estudo modela sequências de transações com LSTM e compara a abordagem a Random Forest com atributos agregados. O resultado mais importante para este projeto não é "LSTM sempre vence", mas a demonstração de que histórico e ordem dos eventos carregam sinais que uma linha isolada pode perder.

**Aplicação:** derivar recência, frequência e desvio em janelas usando apenas dados anteriores à transação analisada.

**Limite:** cartão de crédito e dados próprios; a generalização para Pix precisa de validação.

### 2.3 Dal Pozzolo et al. (2018) - avaliação realista

**Artigo:** [Credit Card Fraud Detection: A Realistic Modeling and a Novel Learning Strategy](https://doi.org/10.1109/TNNLS.2017.2736643), *IEEE Transactions on Neural Networks and Learning Systems*, 29(8), 3784-3797.

O trabalho discute três restrições operacionais decisivas: desbalanceamento, mudança de conceito e atraso entre a transação e a confirmação do rótulo. Também chama atenção para protocolos e métricas próximos do uso real.

**Aplicação:** não executar SMOTE antes da separação treino/teste; documentar a origem do rótulo; evitar validação aleatória como única evidência; discutir o custo de falso negativo e falso positivo.

**Limite:** os rótulos e o fluxo operacional não são os mesmos do MED ou de uma instituição Pix.

### 2.4 Carcillo et al. (2021) - combinação supervisionada e não supervisionada

**Artigo:** [Combining unsupervised and supervised learning in credit card fraud detection](https://doi.org/10.1016/j.ins.2019.05.042), *Information Sciences*, 557, 317-331.

O artigo combina escores de anomalia contextual com classificação supervisionada. A ideia é útil porque fraude nova pode não repetir perfeitamente os exemplos rotulados, enquanto o componente supervisionado aproveita padrões conhecidos.

**Aplicação:** o escopo atual pode manter XGBoost como modelo principal e registrar detecção de anomalia como extensão, não como requisito de maio.

**Limite:** maior complexidade operacional e risco de confundir anomalia com fraude.

## 3. Síntese comparativa

| Tema | Evidência da literatura | Decisão para o TCC |
|---|---|---|
| classe rara | acurácia pode ocultar falha na classe de interesse | relatar AUC-PR, precisão, recall, F1 e matriz de confusão |
| dependência temporal | sequência e agregações históricas são informativas | construir atributos apenas com passado disponível |
| concept drift | o comportamento muda | preferir separação temporal e registrar período dos dados |
| rótulo atrasado | confirmação pode chegar depois | discutir limite do `isFraud` e evitar linguagem de certeza |
| anomalia x fraude | comportamento raro não é necessariamente ilícito | separar escore de risco de conclusão jurídica |
| domínio | resultados de cartão não provam desempenho em Pix | declarar IEEE-CIS como proxy para prova de conceito |

## 4. Referências organizadas (22)

O arquivo [`../../../monografia/referencias.bib`](../../../monografia/referencias.bib) pode ser importado no Zotero ou enviado diretamente ao Overleaf.

### Pix, MED e contexto bancário

1. Banco Central do Brasil. [Resolução BCB nº 1/2020 - Regulamento do Pix](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=1&tipo=Resolu%C3%A7%C3%A3o+BCB). Fonte normativa consolidada.
2. Banco Central do Brasil. [Resolução BCB nº 103/2021](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?lang=pt&numero=103&tipo=Resolu%C3%A7%C3%A3o+BCB). Criação do MED.
3. Banco Central do Brasil. [Resolução BCB nº 403/2024](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=403&tipo=Resolu%C3%A7%C3%A3o+BCB). Alteração específica; não é a criação do MED.
4. Banco Central do Brasil. [Guia do MED, versão 4.3](https://www.bcb.gov.br/content/estabilidadefinanceira/pix/Guia_MED.pdf). Procedimentos e versão operacional.
5. Banco Central do Brasil. [Pix em números](https://www.bcb.gov.br/estabilidadefinanceira/estatisticaspix). Estatísticas dinâmicas; citar período.
6. Banco Central do Brasil. [Meios de pagamento mais utilizados em 2024](https://www.bcb.gov.br/detalhenoticia/20673/noticia). Contexto de adoção.
7. FEBRABAN; Deloitte. [Pesquisa Febraban de Tecnologia Bancária 2024](https://cmsarquivos.febraban.org.br/Arquivos/documentos/PDF/Pesquisa%20Febraban%20de%20Tecnologia%20Banc%C3%A1ria%202024.pdf). Evidência setorial com amostras por gráfico.

### Dataset, modelos, desbalanceamento e métricas

8. IEEE-CIS; Vesta. [IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection/data). Dataset e descrição oficial da competição.
9. Breiman (2001). [Random Forests](https://doi.org/10.1023/A:1010933404324). Modelo comparador.
10. Chen e Guestrin (2016). [XGBoost: A Scalable Tree Boosting System](https://doi.org/10.1145/2939672.2939785). Modelo principal.
11. Chawla et al. (2002). [SMOTE: Synthetic Minority Over-sampling Technique](https://doi.org/10.1613/jair.953). Reamostragem da classe minoritária.
12. Saito e Rehmsmeier (2015). [The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets](https://doi.org/10.1371/journal.pone.0118432). Justificativa para AUC-PR.

### Fraude financeira

13. Abdallah, Maarof e Zainal (2016). [Fraud detection system: A survey](https://doi.org/10.1016/j.jnca.2016.04.007).
14. Jurgovsky et al. (2018). [Sequence classification for credit-card fraud detection](https://doi.org/10.1016/j.eswa.2018.01.037).
15. Dal Pozzolo et al. (2018). [Credit Card Fraud Detection: A Realistic Modeling and a Novel Learning Strategy](https://doi.org/10.1109/TNNLS.2017.2736643).
16. Carcillo et al. (2021). [Combining unsupervised and supervised learning in credit card fraud detection](https://doi.org/10.1016/j.ins.2019.05.042).

### Explicabilidade e RAG

17. Lundberg e Lee (2017). [A Unified Approach to Interpreting Model Predictions](https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html). Fundamento de SHAP.
18. Lewis et al. (2020). [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://papers.nips.cc/paper_files/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). Arquitetura RAG.
19. Reimers e Gurevych (2019). [Sentence-BERT](https://aclanthology.org/D19-1410/). Embeddings de sentenças.
20. Karpukhin et al. (2020). [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550/). Recuperação densa.
21. Johnson, Douze e Jégou (2021). [Billion-scale similarity search with GPUs](https://doi.org/10.1109/TBDATA.2019.2921572). Base técnica do FAISS.
22. Es et al. (2024). [RAGAS: Automated Evaluation of Retrieval Augmented Generation](https://aclanthology.org/2024.eacl-demo.16/). Avaliação de pipelines RAG.

## 5. O que ainda precisa ser levantado depois de maio

- literatura específica sobre fraude em pagamentos instantâneos brasileiros com dados e método auditáveis;
- estudos de explicações de risco avaliadas por profissionais do domínio;
- requisitos institucionais/ABNT e política de uso de IA da faculdade;
- fonte de dados Pix anonimizada ou estratégia formal de validação externa.

Essas lacunas não invalidam a prova de conceito, mas delimitam as conclusões que o TCC pode sustentar.
