# Screenshots das evidências no LangSmith

Capturas exigidas pelo enunciado (seção "Resultados Finais" do README principal).
Salve os arquivos PNG nesta pasta com os nomes abaixo; o README raiz já os referencia.

| Arquivo | O que mostrar | Onde capturar |
|---|---|---|
| `01-evaluate-aprovado.png` | Terminal com `python src/evaluate.py` mostrando `✅ STATUS: APROVADO` e as 5 métricas ≥ 0.8 | terminal |
| `02-dataset-15-exemplos.png` | Dataset `<LANGSMITH_PROJECT>-eval` com 15 exemplos | LangSmith → Datasets & Experiments |
| `03-prompt-v2-hub.png` | Prompt `<username>/bug_to_user_story_v2` publicado como público, com tags/descrição | LangSmith → Prompts |
| `04-tracing-exemplo-1.png` | Trace detalhado de uma execução (system + human prompt e resposta) | LangSmith → Tracing Projects → `<LANGSMITH_PROJECT>` |
| `05-tracing-exemplo-2.png` | Idem, outro exemplo (bug médio) | idem |
| `06-tracing-exemplo-3.png` | Idem, outro exemplo (bug complexo) | idem |
