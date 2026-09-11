"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

HUB_PROMPT = "leonanluppi/bug_to_user_story_v1"
LOCAL_KEY = "bug_to_user_story_v1"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "bug_to_user_story_v1.yml"


def _message_template(message) -> str:
    """Extrai o texto do template de uma mensagem do ChatPromptTemplate."""
    prompt = getattr(message, "prompt", None)
    if prompt is not None and hasattr(prompt, "template"):
        return prompt.template
    return str(getattr(message, "content", message))


def _split_system_user(prompt) -> tuple[str, str]:
    """Separa system_prompt e user_prompt de um ChatPromptTemplate (ou PromptTemplate)."""
    system_prompt, user_prompt = "", ""
    for message in getattr(prompt, "messages", []):
        kind = type(message).__name__
        text = _message_template(message)
        if kind.startswith("System"):
            system_prompt = text
        elif kind.startswith("Human"):
            user_prompt = text
    if not system_prompt and hasattr(prompt, "template"):  # PromptTemplate simples
        system_prompt = prompt.template
    return system_prompt, user_prompt


def _hub_metadata(prompt_name: str) -> dict:
    """Descrição e tags publicadas no Hub (best effort: não falha o pull se indisponível)."""
    try:
        from langsmith import Client
        info = Client().get_prompt(prompt_name)
        return {"description": info.description or "", "tags": list(info.tags or [])}
    except Exception:
        return {"description": "", "tags": []}


def pull_prompts_from_langsmith():
    """Faz pull do prompt v1 do Hub e devolve o dicionário salvo em YAML (ou None em erro)."""
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return None

    print(f"Puxando prompt do LangSmith Hub: {HUB_PROMPT}")
    try:
        prompt = hub.pull(HUB_PROMPT)
    except Exception as e:
        print(f"❌ Falha ao puxar '{HUB_PROMPT}': {e}")
        print("   Verifique LANGSMITH_API_KEY e LANGSMITH_ENDPOINT (o prompt está na região US:")
        print("   https://api.smith.langchain.com).")
        return None

    system_prompt, user_prompt = _split_system_user(prompt)
    meta = _hub_metadata(HUB_PROMPT)
    print(f"   ✓ Prompt carregado ({type(prompt).__name__}, variáveis: {prompt.input_variables})")

    data = {
        LOCAL_KEY: {
            "description": meta["description"] or "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "source": HUB_PROMPT,
            "pulled_at": date.today().isoformat(),
            "tags": meta["tags"] or ["bug-analysis", "user-story", "product-management"],
        }
    }

    if not save_yaml(data, str(OUTPUT_FILE)):
        return None
    print(f"   ✓ Salvo em {OUTPUT_FILE.relative_to(OUTPUT_FILE.parent.parent)}")
    return data


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")
    data = pull_prompts_from_langsmith()
    if not data:
        return 1

    prompt = data[LOCAL_KEY]
    print("\nSystem prompt puxado:")
    print("-" * 50)
    print(prompt["system_prompt"].rstrip())
    print("-" * 50)
    print(f"User prompt: {prompt['user_prompt']!r}")
    print("\nPróximo passo: refatore o prompt em prompts/bug_to_user_story_v2.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
