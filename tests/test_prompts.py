"""
Testes automatizados para validação de prompts.
"""
import json
import re
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

ROOT = Path(__file__).parent.parent
PROMPT_FILE = ROOT / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"
DATASET_FILE = ROOT / "datasets" / "bug_to_user_story.jsonl"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def prompt() -> dict:
    data = load_prompts(str(PROMPT_FILE))
    assert PROMPT_KEY in data, f"chave '{PROMPT_KEY}' ausente em {PROMPT_FILE.name}"
    return data[PROMPT_KEY]


@pytest.fixture(scope="module")
def full_text(prompt) -> str:
    return f"{prompt.get('system_prompt', '')}\n{prompt.get('user_prompt', '')}"


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt
        assert isinstance(prompt["system_prompt"], str)
        assert prompt["system_prompt"].strip(), "system_prompt está vazio"

    def test_prompt_has_role_definition(self, prompt):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt["system_prompt"]
        assert re.search(r"Você é um[a]? [A-Za-zÀ-ú ]+", system_prompt), "persona não definida"
        assert "Product Manager" in system_prompt

    def test_prompt_mentions_format(self, full_text):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        assert "Markdown" in full_text
        for part in ("Como um", "eu quero", "para que"):
            assert part in full_text, f"template de user story sem '{part}'"
        assert "Critérios de Aceitação" in full_text

    def test_prompt_has_few_shot_examples(self, prompt):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt["system_prompt"]
        examples = re.findall(r"### Exemplo \d", system_prompt)
        assert len(examples) >= 2, "são necessários pelo menos 2 exemplos few-shot"
        # cada exemplo tem entrada (relato) e saída (user story)
        assert system_prompt.count("Relato de bug:") >= 2
        assert system_prompt.count("User Story:") >= 2

    def test_prompt_no_todos(self, prompt):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        serialized = yaml.dump(prompt, allow_unicode=True)
        assert "[TODO]" not in serialized
        # "TODO" como palavra isolada (case-sensitive: "todos"/"método" em pt-br não contam)
        assert not re.search(r"\bTODO\b", serialized), "há um TODO esquecido no prompt"

    def test_minimum_techniques(self, prompt):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt.get("techniques_applied", [])
        assert isinstance(techniques, list)
        assert len(techniques) >= 2, f"mínimo de 2 técnicas, encontradas: {len(techniques)}"
        assert any("few-shot" in t.lower() for t in techniques), "Few-shot Learning é obrigatória"
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, errors

    def test_prompt_variable_only_in_user_prompt(self, prompt):
        """Corrige o defeito da v1: {bug_report} só no user_prompt, nunca duplicado no system."""
        assert "{bug_report}" in prompt["user_prompt"]
        assert "{bug_report}" not in prompt["system_prompt"]

    def test_few_shot_examples_not_in_eval_dataset(self, prompt):
        """Os exemplos few-shot não podem vir do dataset de avaliação (evita vazamento de dados)."""
        system_prompt = prompt["system_prompt"]
        rows = [json.loads(l) for l in DATASET_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
        leaked = [r["inputs"]["bug_report"][:60] for r in rows
                  if r["inputs"]["bug_report"].splitlines()[0] in system_prompt]
        assert not leaked, f"bugs do dataset usados como exemplo: {leaked}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
