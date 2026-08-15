# Anotações da Metodologia — TCC Fraude Pix

Registro compartilhado de entendimentos importantes discutidos ao longo do cronograma.
Objetivo: virar base direta de parágrafos do TCC (principalmente Capítulo 3 — Metodologia) sem precisar reconstruir o raciocínio depois. Preencher juntos (Letícia e Lucas) conforme as tarefas do [cronograma](https://letalves.github.io/tcc-fraude-cartao/) forem concluídas.

---

## Maio — Fundação do projeto

### Tarefa: Ler a proposta e entender a metodologia (m1_p1_0a)

- **SHAP explica o quê**: aponta quais variáveis da transação mais influenciaram a decisão do modelo. É a explicação técnica, específica de cada transação.
- **RAG explica o que isso significa**: busca documentos regulatórios (BACEN, FEBRABAN) e descrições de padrões de fraude compatíveis com o que o SHAP apontou, e gera a explicação em linguagem natural para o usuário/analista.
- **Frase-chave para o Capítulo 3**: SHAP = *o quê* (quais variáveis pesaram); RAG = *o que isso significa* (contexto regulatório/humano). Sem o SHAP, o RAG não sabe o que buscar — as duas camadas são complementares, não substitutas.

<!-- Próxima entrada: tarefa m1_p1_0b (dataset IEEE-CIS) -->
