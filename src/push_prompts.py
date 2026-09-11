"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILES = {
    # nome no Hub -> arquivo local. A v1 (baseline) também é publicada para permitir a
    # comparação v1 vs v2 no dashboard, como no exemplo do enunciado.
    "bug_to_user_story_v2": ROOT / "prompts" / "bug_to_user_story_v2.yml",
    "bug_to_user_story_v1": ROOT / "prompts" / "bug_to_user_story_v1.yml",
}


def _slug(text: str) -> str:
    return text.lower().replace(" ", "-")


def _build_readme(prompt_data: dict) -> str:
    techniques = prompt_data.get("techniques_applied", [])
    lines = [f"# {prompt_data.get('version', '')} — {prompt_data.get('description', '')}", ""]
    if techniques:
        lines += ["## Técnicas de Prompt Engineering aplicadas", ""]
        lines += [f"- {t}" for t in techniques]
        lines.append("")
    lines.append("Desafio MBA IA (FullCycle): Pull, Otimização e Avaliação de Prompts com LangChain/LangSmith.")
    return "\n".join(lines)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    full_name = f"{username}/{prompt_name}"

    template = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system_prompt"]),
        ("human", prompt_data.get("user_prompt") or "{bug_report}"),
    ])

    techniques = list(prompt_data.get("techniques_applied", []))
    tags = list(dict.fromkeys(list(prompt_data.get("tags", [])) + [_slug(t) for t in techniques]))
    description = prompt_data.get("description", "")
    if techniques:
        description = f"{description} | Técnicas: {', '.join(techniques)}"

    try:
        url = hub.push(
            full_name,
            template,
            new_repo_is_public=True,
            new_repo_description=description[:250],
            readme=_build_readme(prompt_data),
            tags=tags,
        )
        print(f"   ✓ {full_name} publicado (público)")
        print(f"     URL: {url}")
        print(f"     Tags: {', '.join(tags)}")
        return True
    except Exception as e:
        print(f"   ❌ Falha no push de {full_name}: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    _, errors = validate_prompt_structure(prompt_data)
    system_prompt = prompt_data.get("system_prompt", "") or ""
    user_prompt = prompt_data.get("user_prompt", "") or ""
    if "{bug_report}" not in user_prompt:
        errors.append("user_prompt deve conter a variável {bug_report}")
    if "{bug_report}" in system_prompt:
        errors.append("system_prompt não deve repetir {bug_report} (duplicação herdada da v1)")
    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    ok_count = 0
    for prompt_name, file_path in PROMPT_FILES.items():
        print(f"\n{prompt_name}  ({file_path.relative_to(ROOT)})")
        data = load_yaml(str(file_path))
        if not data or prompt_name not in data:
            print(f"   ⚠️  arquivo ausente ou sem a chave '{prompt_name}', pulando")
            continue
        prompt_data = data[prompt_name]

        if prompt_name.endswith("_v2"):
            is_valid, errors = validate_prompt(prompt_data)
            if not is_valid:
                print("   ❌ Prompt inválido:")
                for err in errors:
                    print(f"      - {err}")
                return 1
            print("   ✓ Validação OK")

        if push_prompt_to_langsmith(prompt_name, prompt_data):
            ok_count += 1

    print(f"\n{ok_count}/{len(PROMPT_FILES)} prompts publicados.")
    print("Confira em: https://smith.langchain.com/prompts")
    print("Próximo passo: python src/evaluate.py")
    return 0 if ok_count and ok_count >= 1 and "bug_to_user_story_v2" in PROMPT_FILES else 1


if __name__ == "__main__":
    sys.exit(main())
