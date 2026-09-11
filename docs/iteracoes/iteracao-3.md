# Iteração 3 — consequências operacionais e exemplos em bloco de código (ensaio local)

Data: 2026-09-11 · Modelo de resposta: gemini-3.5-flash-lite · Juiz: gemini-3.6-flash
Método: mesmas funções de `src/metrics.py` e mesmo dataset de `src/evaluate.py`, lendo o prompt
do YAML local (ensaio antes do push ao Hub).

Mudanças em relação à iteração 2: critérios de consequência operacional (confirmação/notificação ao
usuário, log de auditoria, comportamento em falha, limites de tempo/quantidade); persona igual ao
papel citado no relato; nos bugs complexos, exemplos técnicos em blocos de código, camadas de cache
com TTL e parâmetros de processamento em lote. Pior F1 individual: 0.86 (#10).

## Métricas

| Métrica | Score | ≥ 0.8 |
|---|---|---|
| Helpfulness | 0.9903 | ✓ |
| Correctness | 0.9609 | ✓ |
| F1-Score | 0.9338 | ✓ |
| Clarity | 0.9927 | ✓ |
| Precision | 0.9880 | ✓ |
| **Média** | **0.9731** | APROVADO |

## Por exemplo

| # | Complexidade | F1 | P | R | Clarity | Precision |
|---|---|---|---|---|---|---|
| 1 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 |
| 2 | simple | 0.97 | 0.95 | 1.00 | 0.95 | 0.97 |
| 3 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | simple | 0.92 | 0.95 | 0.90 | 1.00 | 0.98 |
| 5 | simple | 0.95 | 1.00 | 0.90 | 0.99 | 1.00 |
| 6 | medium | 0.89 | 0.95 | 0.83 | 1.00 | 0.97 |
| 7 | medium | 0.97 | 0.95 | 1.00 | 1.00 | 0.98 |
| 8 | medium | 0.92 | 1.00 | 0.85 | 1.00 | 1.00 |
| 9 | medium | 0.90 | 0.95 | 0.85 | 1.00 | 1.00 |
| 10 | medium | 0.86 | 1.00 | 0.75 | 0.95 | 0.98 |
| 11 | medium | 0.90 | 0.95 | 0.85 | 1.00 | 0.98 |
| 12 | medium | 0.92 | 1.00 | 0.85 | 1.00 | 1.00 |
| 13 | complex | 0.97 | 1.00 | 0.95 | 1.00 | 1.00 |
| 14 | complex | 0.94 | 0.95 | 0.93 | 1.00 | 0.98 |
| 15 | complex | 0.90 | 0.95 | 0.85 | 1.00 | 1.00 |

