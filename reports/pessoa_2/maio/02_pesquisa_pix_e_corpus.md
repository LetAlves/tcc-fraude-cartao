# Pesquisa Pix, regulação e corpus documental

Data de acesso e conferência: **15/08/2026**.

## 1. Achado principal: a norma indicada no cronograma estava errada

O cronograma mencionava "Resolução BCB nº 403/2023" como documento do MED. Essa identificação não existe com esse ano e finalidade. A cadeia normativa correta é:

| Documento | O que foi confirmado | Uso no TCC |
|---|---|---|
| [Resolução BCB nº 1, de 12/08/2020](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=1&tipo=Resolu%C3%A7%C3%A3o+BCB) | Regulamento-base e versão consolidada do Pix | fonte normativa principal; registrar data de coleta |
| [Resolução BCB nº 103, de 08/06/2021](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?lang=pt&numero=103&tipo=Resolu%C3%A7%C3%A3o+BCB) | Introduziu a seção do Mecanismo Especial de Devolução; efeitos em novembro de 2021 | fonte histórica para a criação do MED |
| [Resolução BCB nº 402, de 22/07/2024](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=402&tipo=Resolu%C3%A7%C3%A3o+BCB) | Alterou dispositivos do regulamento, inclusive a redação do MED | fonte de alteração normativa de 2024 |
| [Resolução BCB nº 403, de 22/07/2024](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=403&tipo=Resolu%C3%A7%C3%A3o+BCB) | Acrescentou, entre outros ajustes, o que não é considerado falha operacional para devolução | não apresentar como norma criadora do MED |
| [Guia do MED, versão 4.3](https://www.bcb.gov.br/content/estabilidadefinanceira/pix/Guia_MED.pdf) | Guia operacional atual disponibilizado pelo BCB | corpus atual; guardar versão e hash do arquivo |

O próprio [comunicado do BCB sobre a criação do MED](https://www.bcb.gov.br/detalhenoticia/554/noticia) informa que a norma é a Resolução nº 103. A versão consolidada da Resolução nº 1 também marca a seção como incluída pela nº 103.

### Consequência metodológica

O corpus não deve guardar apenas "a resolução do MED" sem data. É necessário distinguir:

- origem histórica do mecanismo;
- texto consolidado vigente na data da consulta;
- alterações posteriores;
- guia operacional com número de versão.

Prazos e procedimentos mudam. Uma frase como "o usuário tem cerca de 80 horas" não deve entrar no TCC sem fonte e data; ela confundia **80 dias**, presente em versões anteriores de material ao usuário, com outro prazo. A implementação deve recuperar o trecho vigente e exibir a data da regra.

## 2. Contexto Pix sustentado por fonte primária

O Banco Central informa que, em 2024, o Pix foi o instrumento de pagamento que mais cresceu em quantidade de transações: **52%**, alcançando **47% das transações de pagamento sem espécie no último trimestre do ano**. A fonte é a notícia oficial ["Confira quais os meios de pagamentos mais utilizados no Brasil em 2024"](https://www.bcb.gov.br/detalhenoticia/20673/noticia), baseada nas Estatísticas de Pagamentos de Varejo e de Cartões.

A página [Pix em números](https://www.bcb.gov.br/estabilidadefinanceira/estatisticaspix) é dinâmica e deve ser tratada como fonte atualizável. Na redação acadêmica, qualquer número retirado dela precisa indicar mês/ano de referência, não apenas a data de acesso.

Esses dados justificam relevância e escala; eles não medem, por si sós, a incidência de fraude. O texto não deve transformar crescimento de uso em crescimento de fraude sem uma série estatística específica.

## 3. Pesquisa FEBRABAN de Tecnologia Bancária 2024

Foi conferido o PDF oficial completo da [Pesquisa Febraban de Tecnologia Bancária 2024](https://cmsarquivos.febraban.org.br/Arquivos/documentos/PDF/Pesquisa%20Febraban%20de%20Tecnologia%20Banc%C3%A1ria%202024.pdf), produzido com a Deloitte. Ele é um relatório setorial sobre estratégia e investimento em tecnologia, não uma norma e não um levantamento da taxa de fraude Pix.

Evidências úteis, sempre acompanhadas da amostra declarada no relatório:

| Página | Evidência | Amostra | Leitura correta |
|---:|---|---:|---|
| 16 | 58% apontaram estratégias de detecção e resposta a ameaças como investimento de cibersegurança em 2024 | 24 bancos | detecção e resposta são prioridades do setor |
| 22 | 73% declararam detecção de fraude e lavagem de dinheiro entre os casos de uso de IA | 22 bancos | sustenta a pertinência de IA para o domínio; não é taxa de adoção de um algoritmo específico |
| 40 | previsão de R$ 1,3 bilhão em projetos regulatórios de Pix em 2024, alta de 34% sobre 2023 | 15 bancos | mostra esforço tecnológico/regulatório; não representa perdas por fraude |

Limitações: respostas múltiplas, amostras diferentes entre gráficos e população composta por bancos participantes da pesquisa. Os percentuais não devem ser generalizados automaticamente para todas as instituições financeiras brasileiras.

## 4. Corpus recomendado para o RAG

### Núcleo obrigatório

1. Resolução BCB nº 1/2020, texto consolidado e data de extração;
2. Resolução BCB nº 103/2021, para histórico do MED;
3. Guia do MED com versão explícita;
4. página de segurança do Pix e perguntas frequentes oficiais do BCB;
5. Pesquisa FEBRABAN 2024, apenas para contexto setorial;
6. artigos científicos selecionados sobre fraude, desbalanceamento e explicabilidade.

### Fontes complementares

- alterações normativas posteriores, cada qual com vigência;
- Estatísticas de Pagamentos de Varejo do BCB;
- materiais públicos de prevenção a golpes, desde que o emissor e a data sejam preservados.

### Fontes que não devem virar verdade normativa

- posts sem autoria;
- matérias jornalísticas quando há uma fonte primária disponível;
- respostas de fóruns sobre o significado das colunas IEEE-CIS;
- snippets de buscador;
- texto gerado por LLM sem fonte verificável.

## 5. Registro de ingestão proposto

```yaml
document_id: bcb-resolucao-1-2020-consolidada
title: Regulamento do Pix
issuer: Banco Central do Brasil
document_type: regulation
source_url: https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=1&tipo=Resolu%C3%A7%C3%A3o+BCB
published_at: 2020-08-12
retrieved_at: 2026-08-15
effective_from: 2020-08-12
effective_to: null
version_label: consolidada-em-2026-08-15
norm_status: vigente-com-alteracoes
text_sha256: preencher-na-ingestao
```

O arquivo original pode permanecer fora do Git quando houver restrição de redistribuição ou tamanho. Nesse caso, versionam-se URL, metadados, hash e um script reprodutível de coleta.

## 6. Como esses documentos entram na explicação

O relatório FEBRABAN pode sustentar uma frase sobre investimento e uso de IA no setor. A resolução e o Guia do MED podem sustentar uma frase sobre regras e procedimentos. Nenhum deles, isoladamente, prova que uma transação específica foi fraudulenta.

A resposta do sistema deve manter as evidências separadas:

- **evidência do modelo**: escore, limiar e SHAP;
- **evidência documental**: trecho, emissor, versão e página/seção;
- **inferência do sistema**: explicação em linguagem natural, claramente identificada como interpretação.

## 7. Decisão recomendada

Substituir em todo o planejamento a expressão "Resolução BCB nº 403/2023" por **"Regulamento do Pix (Resolução BCB nº 1/2020 consolidada), Resolução BCB nº 103/2021 e Guia do MED vigente"**. Manter a nº 403/2024 apenas quando o texto discutir a alteração específica de 2024.
