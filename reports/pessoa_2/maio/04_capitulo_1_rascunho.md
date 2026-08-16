# Capítulo 1 - Introdução (rascunho)

> Estado: primeira versão para revisão de Letícia, Lucas e orientador. As citações estão ligadas a `monografia/referencias.bib`. O texto não deve ser apresentado como versão final antes da adequação ao template e às regras da instituição.

## 1.1 Contextualização

O Pix consolidou-se como infraestrutura relevante do sistema de pagamentos brasileiro por oferecer transferências e pagamentos instantâneos em disponibilidade contínua. Em 2024, foi o instrumento de pagamento com maior crescimento em quantidade de transações no país, com aumento de 52%, e respondeu por 47% das transações de pagamento sem uso de espécie no último trimestre do ano (BANCO CENTRAL DO BRASIL, 2025). Essa escala amplia a importância de mecanismos capazes de identificar rapidamente comportamentos de risco sem comprometer de forma desnecessária operações legítimas.

Fraudes financeiras constituem um problema de classificação particularmente difícil. Os casos confirmados são raros em comparação às operações legítimas, os padrões mudam ao longo do tempo e a confirmação do rótulo pode ocorrer depois da transação. Assim, uma solução pode apresentar alta acurácia global e ainda falhar justamente na classe de maior interesse (ABDALLAH; MAAROF; ZAINAL, 2016; DAL POZZOLO et al., 2018). Métricas voltadas ao desempenho na classe positiva, como precisão, revocação, F1 e área sob a curva precisão-revocação, são mais informativas nesse cenário do que a acurácia isolada (SAITO; REHMSMEIER, 2015).

Além do desempenho preditivo, decisões automatizadas no domínio financeiro exigem rastreabilidade. Um escore alto, sem indicação dos fatores que o influenciaram, oferece pouco suporte a um analista e pode induzir confiança excessiva. SHAP fornece atribuições locais para mostrar como cada variável contribuiu para uma previsão (LUNDBERG; LEE, 2017). Entretanto, a explicação matemática não contém, por si só, o contexto regulatório e operacional do Pix.

Retrieval-Augmented Generation (RAG) permite recuperar trechos de uma coleção documental e fornecê-los a um modelo de linguagem durante a geração da resposta (LEWIS et al., 2020). No presente trabalho, essa abordagem é investigada como complemento, e não substituto, da explicação SHAP: o modelo estima o risco, SHAP registra os fatores da decisão e o RAG busca documentos do Banco Central, literatura científica e fontes setoriais para produzir uma contextualização rastreável em português.

O Banco Central instituiu o Mecanismo Especial de Devolução por meio da Resolução BCB nº 103/2021, posteriormente incorporada e alterada no Regulamento do Pix. Esse histórico ilustra uma exigência central para a base documental: toda explicação regulatória deve preservar fonte, versão e vigência. Um sistema que mistura regras de períodos diferentes pode apresentar uma resposta fluente, porém incorreta.

## 1.2 Problema de pesquisa

Modelos de aprendizado de máquina podem reconhecer padrões complexos em transações, mas sua saída costuma ser técnica e insuficiente para explicar o resultado em linguagem acessível. Em sentido oposto, um modelo de linguagem pode produzir uma narrativa convincente sem fidelidade ao classificador ou à norma aplicável. O desafio é integrar previsão, explicabilidade e recuperação documental sem transformar correlação em causalidade, sem inventar o significado de atributos anonimizados e sem ocultar as limitações do conjunto de dados.

Este projeto usa o conjunto IEEE-CIS Fraud Detection, composto por transações de comércio eletrônico fornecidas pela Vesta. Ele não contém transações Pix e parte de seus atributos é anonimizada. Portanto, o dataset serve como base para uma prova de conceito de classificação de risco e integração técnica; não permite afirmar que o desempenho obtido representa uma operação Pix real.

### Questão de pesquisa

**Como integrar um modelo de detecção de fraude, explicações locais por SHAP e recuperação de documentos por RAG para produzir explicações rastreáveis em português, preservando a fidelidade ao modelo e explicitando as limitações de uma prova de conceito baseada no IEEE-CIS?**

## 1.3 Objetivos

### 1.3.1 Objetivo geral

Desenvolver e avaliar um protótipo híbrido que combine aprendizado de máquina, SHAP e RAG para classificar o risco de fraude em dados transacionais e gerar explicações em português sustentadas por evidências do modelo e por documentos verificáveis relacionados ao contexto Pix brasileiro.

### 1.3.2 Objetivos específicos

1. preparar e caracterizar o dataset IEEE-CIS, documentando desbalanceamento, valores ausentes, anonimização e diferenças em relação ao domínio Pix;
2. treinar e comparar XGBoost, Random Forest e uma linha de base usando métricas adequadas à classe rara;
3. aplicar SHAP para identificar, global e localmente, as variáveis que influenciam as previsões;
4. construir um registro de atributos semânticos que impeça a tradução indevida de colunas anônimas para conceitos Pix;
5. organizar uma base documental versionada com normas e materiais oficiais do Banco Central, literatura científica e fontes setoriais selecionadas;
6. implementar recuperação semântica e geração de explicações que citem os trechos utilizados;
7. avaliar a qualidade da recuperação, a coerência da resposta com SHAP, o suporte documental das afirmações e a clareza para usuários;
8. disponibilizar o código, as decisões metodológicas e instruções de reprodução, respeitando limites de licença e privacidade dos dados.

## 1.4 Justificativa

A Pesquisa Febraban de Tecnologia Bancária 2024 mostra que 73% dos 22 bancos participantes daquela questão declararam usar inteligência artificial em detecção de fraude e lavagem de dinheiro. O mesmo relatório registra estratégias de detecção e resposta entre prioridades de cibersegurança. Esses resultados não medem fraude Pix nem representam todo o sistema financeiro, mas evidenciam a pertinência prática de técnicas de IA no setor (FEBRABAN; DELOITTE, 2024).

No plano acadêmico, a contribuição está na integração controlada de três tipos de evidência. O escore preditivo responde quanto o padrão se aproxima da classe aprendida; SHAP descreve quais entradas influenciaram a decisão; o RAG fornece contexto documental com fonte. A separação explícita dessas evidências pode reduzir explicações genéricas e facilitar a auditoria de cada afirmação.

A proposta também é relevante por tratar limites frequentemente omitidos em protótipos: mudança de distribuição, vazamento de dados ao reamostrar, escolha de métricas, temporalidade das normas e risco de atribuir significado a variáveis anonimizadas. Ao registrar esses limites, o trabalho evita apresentar uma demonstração acadêmica como sistema pronto para decisão financeira em produção.

## 1.5 Delimitação do trabalho

O escopo compreende uma prova de conceito executada sobre o IEEE-CIS, com modelos tabulares, explicações SHAP, índice vetorial local e uma interface demonstrativa. Não fazem parte do escopo:

- implantação em uma instituição financeira;
- processamento de dados pessoais reais de clientes Pix;
- decisão automática de bloqueio, acusação ou devolução;
- validação jurídica da elegibilidade ao MED;
- comprovação de generalização para transações Pix reais;
- comparação exaustiva de todos os modelos de detecção de fraude.

Qualquer dado apresentado ao LLM deve ser anonimizado ou sintético. Documentos regulatórios devem ser recuperados com metadados de versão e vigência. A saída será descrita como apoio explicativo sujeito a revisão humana.

## 1.6 Contribuições esperadas

Espera-se entregar:

1. um pipeline reproduzível de preparação, classificação e explicação;
2. um esquema de evidências que conecte SHAP ao RAG sem inventar semântica;
3. um corpus documental rastreável e temporalmente versionado;
4. um protocolo de avaliação separado para desempenho preditivo, recuperação e fidelidade das explicações;
5. uma discussão transparente sobre a transferência limitada do IEEE-CIS para o contexto Pix.

## 1.7 Organização do trabalho

Além desta introdução, o Capítulo 2 apresentará os fundamentos de fraude financeira, Pix, aprendizado de máquina, explicabilidade e RAG. O Capítulo 3 descreverá dados, preparação, modelos, protocolo experimental, corpus e integração das três camadas. O Capítulo 4 reunirá resultados preditivos, explicações locais, avaliação da recuperação e análise de erros. Por fim, o Capítulo 5 discutirá conclusões, limitações e trabalhos futuros.

## Pontos para a revisão do orientador

- confirmar o título final e a formulação da questão de pesquisa;
- validar se o curso exige hipótese formal;
- aprovar a caracterização do IEEE-CIS como proxy de prova de conceito;
- definir o protocolo de avaliação humana das explicações;
- indicar o manual institucional e o modelo ABNT obrigatório.
