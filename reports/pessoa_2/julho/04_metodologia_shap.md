# Metodologia da Camada 2 — SHAP

Data da redação: **30/08/2026**. Escopo: `m3_p2_5`.

## Objetivo

Definir como as explicações SHAP serão calculadas, verificadas e transformadas em evidência para o RAG. Este documento descreve protocolo; não apresenta valores SHAP nem métricas de modelos que ainda não foram entregues pela Pessoa 1.

## Contrato da camada

**Entrada:** pipeline de pré-processamento congelado, modelo treinado, linha transformada, conjunto de referência, versão das features e escala da saída explicada.

**Saída por transação:** identificador pseudonimizado, valor-base, saída do modelo, contribuição por atributo, valor observado, direção, unidade, versão do modelo, versão do explicador e advertências de domínio.

A verificação de consistência deve testar a propriedade aditiva na escala escolhida:

```text
saída_do_modelo ≈ valor_base + soma(contribuições_SHAP)
```

Para modelos de árvore, será usado `shap.TreeExplainer`. O experimento deve registrar se a saída explicada é margem/log-odds ou probabilidade; contribuições de escalas diferentes não podem ser comparadas como se fossem equivalentes. O conjunto de referência e a configuração de dependência entre atributos também devem ser versionados.

## Protocolo

1. congelar split, pré-processamento, features, modelo e limiar;
2. construir o explicador somente com artefatos derivados do treino;
3. calcular SHAP para uma amostra fixa do teste e para casos representativos: verdadeiro positivo, falso positivo, falso negativo e verdadeiro negativo;
4. verificar aditividade, valores ausentes, ordem das colunas e estabilidade numérica;
5. reportar visão global por média de `|SHAP|`, sem confundi-la com causalidade;
6. reportar explicações locais com valor observado, sinal e magnitude;
7. comparar XGBoost e Random Forest apenas após ambos serem executados no mesmo protocolo;
8. registrar limitações e exemplos em que a explicação não é semanticamente interpretável.

## Ponte SHAP → RAG

Somente features com conceito aprovado no [`../../../config/pix_feature_registry.json`](../../../config/pix_feature_registry.json) podem virar tags de busca documental. O pacote enviado ao retriever deve conter:

- `feature_id` e versão do registro;
- valor observado e unidade;
- contribuição e escala explicada;
- tag conceitual aprovada;
- advertência de que IEEE-CIS não é Pix real.

Features anônimas (`V*`, `C*`, `D*`, `M*`, `id_*`) podem aparecer como importantes para o classificador, mas devem ser narradas como “atributo anonimizado de alta influência”. SHAP não revela seu significado e não autoriza associá-las a conta, chave, dispositivo ou intenção de fraude.

## Avaliação

| Dimensão | Verificação |
|---|---|
| Fidelidade numérica | valor-base + contribuições reconstrói a saída dentro de tolerância |
| Alinhamento | nome, valor e posição da feature coincidem com o pipeline treinado |
| Estabilidade | pequenas perturbações plausíveis não geram narrativa contraditória sem alerta |
| Cobertura | análise inclui acertos e erros das duas classes |
| Segurança semântica | nenhuma causalidade, acusação ou significado anônimo é inventado |
| Integração | tags enviadas ao RAG pertencem ao registro aprovado |

## Limitações obrigatórias no texto final

- SHAP explica o comportamento do modelo, não a causa real da transação.
- Importância global não substitui explicação local.
- Atributos correlacionados podem repartir contribuição de maneira sensível à configuração do explicador.
- Uma explicação fiel pode expor um modelo errado, enviesado ou mal calibrado.
- O domínio IEEE-CIS é comércio eletrônico/cartão e não valida desempenho operacional no Pix.

Referência metodológica principal: Lundberg e Lee (2017), já incluída em `monografia/referencias.bib` como `lundberg2017unified`.
