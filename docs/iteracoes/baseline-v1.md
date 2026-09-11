# Baseline — prompt v1 (ensaio local)

Data: 2026-09-11 · Modelo de resposta: gemini-3.5-flash-lite · Juiz: gemini-3.6-flash
Método: mesmas funções de `src/metrics.py` e mesmo dataset de `src/evaluate.py`, lendo o prompt
do YAML local (ensaio antes do push ao Hub).

Prompt puxado do Hub sem alterações (`{bug_report}` duplicado, sem persona, formato ou exemplos).
Serve de referência para a tabela comparativa v1 vs v2.

## Métricas

| Métrica | Score | ≥ 0.8 |
|---|---|---|
| Helpfulness | 0.9960 | ✓ |
| Correctness | 0.9365 | ✓ |
| F1-Score | 0.8783 | ✓ |
| Clarity | 0.9973 | ✓ |
| Precision | 0.9947 | ✓ |
| **Média** | **0.9606** | APROVADO |

## Por exemplo

| # | Complexidade | F1 | P | R | Clarity | Precision |
|---|---|---|---|---|---|---|
| 1 | simple | 0.92 | 1.00 | 0.85 | 1.00 | 1.00 |
| 2 | simple | 0.97 | 0.95 | 1.00 | 1.00 | 1.00 |
| 3 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | simple | 0.95 | 1.00 | 0.90 | 0.98 | 1.00 |
| 5 | simple | 0.92 | 0.95 | 0.90 | 1.00 | 1.00 |
| 6 | medium | 0.91 | 1.00 | 0.83 | 1.00 | 1.00 |
| 7 | medium | 0.85 | 0.85 | 0.85 | 1.00 | 0.98 |
| 8 | medium | 0.84 | 0.95 | 0.75 | 1.00 | 0.97 |
| 9 | medium | 0.92 | 1.00 | 0.85 | 0.98 | 1.00 |
| 10 | medium | 0.95 | 1.00 | 0.90 | 1.00 | 1.00 |
| 11 | medium | 0.79 | 1.00 | 0.65 | 1.00 | 0.97 |
| 12 | medium | 0.71 | 1.00 | 0.55 | 1.00 | 1.00 |
| 13 | complex | 0.90 | 0.95 | 0.85 | 1.00 | 1.00 |
| 14 | complex | 0.86 | 1.00 | 0.75 | 1.00 | 1.00 |
| 15 | complex | 0.70 | 0.95 | 0.55 | 1.00 | 1.00 |

