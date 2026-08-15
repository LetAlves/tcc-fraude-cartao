# Guia de contribuição

## Fluxo Git

`main` representa o estado integrado do TCC. Não desenvolver diretamente nela. Para cada entrega:

```powershell
git switch main
git pull --ff-only origin main
git switch -c docs/capitulo-1
```

Convenção de branches: `<tipo>/<escopo-curto-em-kebab-case>`.

| Tipo | Uso | Exemplo |
|---|---|---|
| `feat/` | nova funcionalidade | `feat/retriever-faiss` |
| `data/` | carga ou transformação de dados | `data/eda-ieee-cis` |
| `exp/` | experimento reproduzível | `exp/xgboost-baseline` |
| `docs/` | monografia ou documentação | `docs/revisao-rag` |
| `fix/` | correção | `fix/med-norma-correta` |
| `chore/` | manutenção | `chore/atualiza-dependencias` |
| `codex/` | trabalho assistido pelo Codex | `codex/maio-pessoa-2` |

Uma branch deve tratar uma entrega coerente. Trabalho pronto é enviado por pull request, revisado pela outra pessoa e integrado sem reescrever contribuições alheias.

## Commits

Usar mensagens curtas no imperativo e indicar o tipo:

```text
docs: adiciona rascunho do capitulo 1
feat: implementa recuperacao vetorial
fix: corrige referencia normativa do MED
```

Não misturar dados grandes, credenciais ou mudanças sem relação no mesmo commit.

## Pull request

O corpo do PR deve responder:

- qual tarefa do cronograma está sendo atendida;
- o que mudou;
- como foi validado;
- quais resultados e limitações foram encontrados;
- quais decisões ainda dependem da dupla ou do orientador.

Checklist mínimo:

- [ ] arquivos grandes e credenciais continuam fora do Git;
- [ ] fonte e data acompanham afirmações externas;
- [ ] código executa a partir da raiz do repositório;
- [ ] transformação treinada usa apenas dados de treino;
- [ ] experimento registra seed, versão, parâmetros e métricas;
- [ ] texto diferencia fato, inferência e limitação;
- [ ] outra pessoa revisou antes do merge.

## Dados e segredos

- `data/raw/` e `data/processed/` não são versionados;
- tokens Kaggle/LLM ficam em arquivo local ou variável de ambiente;
- `.env`, `kaggle.json` e tokens nunca entram em commit, log, notebook ou captura de tela;
- se uma credencial vazar, revogá-la imediatamente e remover o segredo do histórico;
- exemplos enviados ao LLM devem ser sintéticos ou anonimizados.

## Experimentos

Cada resultado usado na monografia deve registrar:

- hash do commit;
- versão ou hash dos dados;
- estratégia de divisão;
- seed;
- atributos e pré-processamento;
- parâmetros;
- limiar de decisão;
- AUC-PR, precisão, recall, F1 e matriz de confusão;
- tempo e ambiente de execução.

SMOTE ou qualquer reamostragem deve ocorrer somente dentro do treino de cada partição. Ajustes de imputação, escala ou seleção de atributos também devem ser aprendidos no treino.

## Documentação acadêmica

Referências são mantidas em `monografia/referencias.bib`. Fontes normativas precisam de emissor, URL, data, vigência/versão e data de acesso. Alterações na monografia devem compilar no projeto Overleaf e ser revisadas quanto a citações, figuras e referências.
