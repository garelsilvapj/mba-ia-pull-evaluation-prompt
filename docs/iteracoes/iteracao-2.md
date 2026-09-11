# Iteração 2 — critérios complementares, persona de sistema, metas ambiciosas (ensaio local)

Data: 2026-09-11 · Modelo de resposta: gemini-3.5-flash-lite · Juiz: gemini-3.6-flash
Método: mesmas funções de `src/metrics.py` e mesmo dataset de `src/evaluate.py`, lendo o prompt
do YAML local (ensaio antes do push ao Hub).

Mudanças em relação à iteração 1 (ver `iteracao-1.md`): bloco de critérios complementares para
bugs médios (perfil admin, prevenção, acessibilidade, critérios técnicos); persona "o sistema [de
domínio]" para bugs de backend/integração; metas mensuráveis claramente melhores que o estado atual;
regra de não fixar valores de exemplo como critério; nos bugs complexos, exemplos concretos nos
critérios técnicos, tasks em fases e seção `=== MÉTRICAS DE SUCESSO ===`.

## Métricas

| Métrica | Score | ≥ 0.8 |
|---|---|---|
| Helpfulness | 0.9967 | ✓ |
| Correctness | 0.9568 | ✓ |
| F1-Score | 0.9202 | ✓ |
| Clarity | 1.0000 | ✓ |
| Precision | 0.9933 | ✓ |
| **Média** | **0.9734** | APROVADO |

## Por exemplo

| # | Complexidade | F1 | P | R | Clarity | Precision |
|---|---|---|---|---|---|---|
| 1 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 2 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | simple | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 4 | simple | 0.87 | 0.95 | 0.80 | 1.00 | 0.97 |
| 5 | simple | 0.92 | 1.00 | 0.85 | 1.00 | 1.00 |
| 6 | medium | 0.86 | 1.00 | 0.75 | 1.00 | 0.97 |
| 7 | medium | 0.99 | 0.98 | 1.00 | 1.00 | 1.00 |
| 8 | medium | 0.92 | 1.00 | 0.85 | 1.00 | 1.00 |
| 9 | medium | 0.95 | 1.00 | 0.90 | 1.00 | 1.00 |
| 10 | medium | 0.90 | 0.95 | 0.85 | 1.00 | 1.00 |
| 11 | medium | 0.87 | 0.95 | 0.80 | 1.00 | 0.98 |
| 12 | medium | 0.89 | 1.00 | 0.80 | 1.00 | 0.98 |
| 13 | complex | 0.91 | 0.98 | 0.85 | 1.00 | 1.00 |
| 14 | complex | 0.87 | 0.98 | 0.78 | 1.00 | 1.00 |
| 15 | complex | 0.87 | 0.98 | 0.78 | 1.00 | 1.00 |

