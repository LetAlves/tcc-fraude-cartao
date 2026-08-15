# Guia de estudo - arquitetura ML -> SHAP -> RAG

## 1. O problema que o protótipo resolve

O sistema recebe os atributos de uma transação e produz duas saídas distintas:

1. **estimativa de risco**: a camada de machine learning calcula uma probabilidade ou escore de fraude;
2. **explicação apoiada em evidências**: SHAP mostra quais atributos influenciaram aquele escore e o RAG recupera documentos pertinentes para contextualizar a decisão.

O protótipo não determina juridicamente que houve fraude, não substitui a análise de uma instituição financeira e não garante devolução via MED. Sua saída correta é algo como "transação classificada como alto risco segundo o modelo", acompanhada de evidências e limitações.

## 2. As três camadas

### Camada 1 - machine learning

O XGBoost é o modelo principal previsto e o Random Forest funciona como comparador. Ambos aprendem padrões em dados tabulares. A saída deve conter pelo menos:

- identificador da transação;
- versão do modelo e do conjunto de atributos;
- probabilidade estimada;
- limiar usado;
- classe produzida;
- instante da inferência.

Como fraude é rara, acurácia isolada é enganosa. A avaliação deve priorizar AUC-PR, precisão, recall, F1 e matriz de confusão em um limiar escolhido com justificativa. Divisões temporais são preferíveis quando a ordem dos eventos está disponível, porque reduzem vazamento entre passado e futuro.

### Camada 2 - SHAP

SHAP atribui a cada atributo uma contribuição local em relação ao valor-base do modelo. Em termos práticos, responde: **quais entradas elevaram ou reduziram o escore nesta transação?**

SHAP não descobre causalidade, intenção criminosa nem o significado secreto de uma coluna anonimizada. Um valor SHAP alto para `V258` prova apenas que `V258` influenciou o modelo naquele caso. Por isso, a visualização deve preservar:

- valor observado do atributo;
- contribuição e sinal do SHAP;
- valor-base/referência;
- unidade e definição do atributo, quando conhecidas;
- versão do modelo e do explicador.

### Camada 3 - RAG

Retrieval-Augmented Generation combina recuperação de documentos com um modelo de linguagem. O fluxo é:

1. documentos confiáveis são coletados;
2. cada documento é extraído, normalizado e dividido em trechos;
3. trechos viram vetores por um modelo de embeddings;
4. os vetores e seus metadados são indexados;
5. uma consulta recupera os trechos mais relacionados;
6. o LLM recebe a evidência do modelo, os trechos e instruções restritivas;
7. a resposta cita as fontes e explicita quando a evidência é insuficiente.

O **retriever** localiza candidatos; os **embeddings** representam proximidade semântica; o **LLM** organiza uma resposta legível. O banco vetorial não é fonte da verdade: a verdade documental continua no texto original e em seus metadados.

## 3. A ponte segura entre SHAP e RAG

Enviar diretamente `top_features = [V258, C14, id_31]` ao retriever é um erro de arquitetura. Os nomes são opacos e podem recuperar textos irrelevantes por coincidência lexical. A solução recomendada é um **pacote de evidências estruturado**.

Exemplo conceitual:

```json
{
  "transaction_id": 123,
  "risk_score": 0.87,
  "threshold": 0.62,
  "model_version": "xgb-2026-08",
  "evidence": [
    {
      "feature_id": "valor_atipico_conta_proxy",
      "definition_version": "1.0",
      "observed_value": 4.8,
      "unit": "desvios-padrao",
      "shap_value": 0.41,
      "direction": "aumenta_risco",
      "concept_tags": ["valor_atipico", "desvio_comportamental"]
    }
  ]
}
```

O construtor da consulta usa somente `concept_tags` aprovadas. A tabela que define cada atributo derivado deve conter fórmula, fonte, janela temporal, tratamento de ausentes, responsável e versão. Colunas anônimas ainda podem melhorar o classificador, mas aparecem na explicação como "atributo anonimizado de alta influência" e não são usadas para afirmar um padrão Pix específico.

## 4. Ingestão do corpus

Cada trecho indexado deve carregar metadados mínimos:

| Campo | Motivo |
|---|---|
| `document_id` e `chunk_id` | rastreabilidade |
| `title`, `issuer`, `document_type` | identificação da autoridade |
| `published_at`, `effective_from`, `effective_to` | controle temporal |
| `retrieved_at` e `source_url` | reprodutibilidade |
| `page` ou seção | citação verificável |
| `text_sha256` | detectar alteração do conteúdo |
| `norm_status` | vigente, alterada, revogada ou histórica |
| `license_or_access_note` | uso correto do documento |

Normas consolidadas mudam com o tempo. Portanto, a consulta deve poder filtrar a versão válida na data analisada. Sem isso, o RAG pode misturar uma regra de 2021 com outra de 2026 e produzir uma orientação incoerente.

## 5. Recuperação e geração

Configuração inicial recomendada para a prova de conceito:

- embeddings multilíngues com `paraphrase-multilingual-MiniLM-L12-v2` ou modelo equivalente validado em português;
- FAISS local para experimentos reproduzíveis;
- busca vetorial com `top_k` pequeno, seguida de filtro por emissor, tipo e vigência;
- prompt que proíba criar significado para atributo anônimo;
- resposta com afirmação, evidência SHAP, contexto documental, fonte e ressalva;
- temperatura baixa e formato de saída estruturado.

FAISS atende ao protótipo local, mas não oferece sozinho autenticação, auditoria, atualização concorrente ou persistência gerenciada. Essas capacidades seriam necessárias em produção.

## 6. Por que RAG é útil aqui

SHAP descreve a decisão do modelo; não contém conhecimento regulatório. O RAG permite apresentar, ao lado da contribuição técnica, trechos atuais do regulamento do Pix, do Guia do MED ou de estudos setoriais. Isso reduz a dependência da memória paramétrica do LLM e torna a explicação auditável.

O benefício só existe quando o documento recuperado realmente sustenta a frase gerada. RAG não elimina alucinação. Ele troca uma pergunta vaga por um processo verificável: **qual trecho foi recuperado, de qual versão e como ele apoia esta sentença?**

## 7. Avaliação da camada de explicação

Separar a avaliação em quatro níveis:

1. **recuperação**: recall@k, precisão@k e MRR em um conjunto de perguntas com trechos relevantes anotados;
2. **fidelidade ao modelo**: atributos e direções mencionados devem coincidir com o pacote SHAP;
3. **fidelidade documental**: cada afirmação regulatória precisa ser suportada pelo trecho citado;
4. **qualidade humana**: clareza, utilidade, ausência de linguagem acusatória e compreensão por analistas.

RAGAS pode apoiar testes automáticos, mas não substitui a inspeção humana nem uma coleção de referência construída para o domínio Pix.

## 8. Riscos e controles

| Risco | Controle recomendado |
|---|---|
| vazamento de dados pessoais em prompts | anonimização, minimização e uso de exemplos sintéticos |
| inferir semântica de coluna anônima | registro de atributos e bloqueio no construtor de consulta |
| norma desatualizada | metadados de vigência e revisão programada do corpus |
| explicação incompatível com SHAP | validação automática do formato e dos sinais |
| recuperar fonte fraca | priorização BCB -> legislação -> artigos revisados -> relatório setorial |
| confiança excessiva na saída | escore, limiar, limitações e revisão humana visíveis |
| vazamento treino/teste ao usar SMOTE | reamostragem somente dentro das partições de treino |

## 9. Checklist de entendimento

- [x] Sei distinguir previsão de risco, explicação local e contexto documental.
- [x] Sei que SHAP não é causal e RAG não é uma base de verdade.
- [x] Sei por que colunas anônimas não podem virar conceitos Pix por suposição.
- [x] Sei como documentos se tornam chunks, embeddings e resultados recuperados.
- [x] Sei quais metadados preservam versão, fonte e vigência.
- [x] Sei como avaliar recuperação, fidelidade ao modelo e fidelidade documental.

## Referências centrais

- Lundberg e Lee, [A Unified Approach to Interpreting Model Predictions](https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html), 2017.
- Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://papers.nips.cc/paper_files/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html), 2020.
- Reimers e Gurevych, [Sentence-BERT](https://aclanthology.org/D19-1410/), 2019.
- Karpukhin et al., [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906), 2020.
- Es et al., [RAGAS: Automated Evaluation of Retrieval Augmented Generation](https://aclanthology.org/2024.eacl-demo.16/), 2024.
