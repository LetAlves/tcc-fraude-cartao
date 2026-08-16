# Ata — Mapeamento IEEE-CIS → Pix (tarefa m1_ab_0)

**Data:** 16/08/2026
**Participantes:** Letícia e Lucas (ambos confirmaram nesta data).

## Contexto

Leitura técnica e auditoria do dicionário de dados feitas por Lucas em
[`reports/pessoa_2/maio/05_mapeamento_e_kickoff.md`](../pessoa_2/maio/05_mapeamento_e_kickoff.md).
Esta ata registra a validação de Letícia sobre os pontos levantados lá.

## Decisões confirmadas pela dupla

1. **Cobertura de identidade:** adotar ~24,4% (recalculado direto dos CSVs), substituindo o
   ~60% que estava no dicionário antigo.
2. **Regra de linguagem no mapeamento:** todo atributo do IEEE-CIS usado como analogia ao Pix
   deve ser descrito como "papel analítico análogo", nunca como equivalência direta
   (ex.: proibido afirmar que `C1` "mede contas Pix do destinatário").
3. **Atributos derivados aprovados para implementação em junho**
   (`src/features/pix_features.py`), com as ressalvas já documentadas na seção 4 de
   `05_mapeamento_e_kickoff.md`:
   - `valor_atipico_cartao_proxy`
   - `frequencia_recente_cartao_proxy`
   - `dispositivo_raro_cartao_proxy`
   - `posicao_ciclo_diario_relativa`

## Pendências

- Tarefa m1_ab_1 (reunião de kickoff) segue em aberto: dia da reunião semanal, Overleaf x
  Google Docs, modelo de embeddings, LLM local x remoto, protocolo de revisão de fontes,
  marcos internos e template institucional ainda não foram decididos.
