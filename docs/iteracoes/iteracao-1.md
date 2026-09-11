# Iteração 1 — prompt v2 inicial (ensaio local)

Data: 2026-09-11 · Modelo de resposta: gemini-3.5-flash-lite · Juiz: gemini-3.6-flash
Método: mesmas funções de `src/metrics.py` e mesmo dataset de `src/evaluate.py`, lendo o prompt
do YAML local (ensaio antes do push ao Hub).

## Métricas

| Métrica | Score | ≥ 0.8 |
|---|---|---|
| Helpfulness | 0.9847 | ✓ |
| Correctness | 0.9210 | ✓ |
| F1-Score | 0.8639 | ✓ |
| Clarity | 0.9913 | ✓ |
| Precision | 0.9780 | ✓ |
| **Média** | **0.9478** | APROVADO |

## Por exemplo

| # | Complexidade | F1 | P | R | Clarity | Precision |
|---|---|---|---|---|---|---|
| 1 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 2 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | simple | 0.74 | 0.85 | 0.65 | 0.98 | 0.87 |
| 5 | simple | 0.95 | 1.00 | 0.90 | 1.00 | 0.98 |
| 6 | medium | 0.65 | 0.80 | 0.55 | 1.00 | 0.93 |
| 7 | medium | 0.82 | 0.85 | 0.80 | 1.00 | 0.95 |
| 8 | medium | 0.84 | 0.95 | 0.75 | 0.96 | 0.98 |
| 9 | medium | 0.92 | 1.00 | 0.85 | 1.00 | 1.00 |
| 10 | medium | 0.86 | 1.00 | 0.75 | 1.00 | 0.98 |
| 11 | medium | 0.81 | 0.95 | 0.70 | 1.00 | 0.98 |
| 12 | medium | 0.75 | 1.00 | 0.60 | 1.00 | 1.00 |
| 13 | complex | 0.94 | 1.00 | 0.88 | 1.00 | 1.00 |
| 14 | complex | 0.87 | 0.98 | 0.78 | 0.98 | 1.00 |
| 15 | complex | 0.82 | 1.00 | 0.70 | 0.95 | 1.00 |

## Diagnóstico (a partir do raciocínio dos juízes)

F1 é a métrica mais baixa e a perda vem quase toda do **recall**:
- Bugs médios: a referência traz um segundo bloco de critérios (acessibilidade no #12,
  prevenção/concorrência no #11, perfil admin no #8, critérios técnicos no #10) que a v2 omitiu.
- #6 (webhook): persona "cliente" em vez de "o sistema de e-commerce"; critérios genéricos.
- #7 (relatório lento): meta "menos de 120 s" copiada do timeout atual; a referência define
  meta ambiciosa (< 30 s).
- #4: valor de exemplo do relato fixado como regra ("42") em vez da regra geral (contador = total real).
- Complexos (#14, #15): faltaram exemplos concretos nos critérios técnicos (query SQL, protocolo
  de upload, estrutura de operação) e a seção de métricas de sucesso (antes vs depois).

## Mudanças para a iteração 2

1. Bloco de **critérios complementares** para bugs médios (outro perfil, prevenção, acessibilidade,
   critérios técnicos) quando o relato der base.
2. Regra de persona "o sistema [de domínio]" para bugs de backend/integração/autorização.
3. Regra de **metas mensuráveis ambiciosas**, claramente melhores que o estado atual.
4. Regra de **não fixar valores de exemplo** como critério; descrever a regra geral.
5. Bugs complexos: critérios técnicos com exemplos concretos (query, protocolo, estrutura de
   dados), tasks agrupadas em fases e seção `=== MÉTRICAS DE SUCESSO ===` quando houver números.
