"""
Avaliação do prompt BASELINE (v1) com as MESMAS métricas e o MESMO dataset de src/evaluate.py.

src/evaluate.py (fornecido pelo desafio, não alterado) avalia apenas {username}/bug_to_user_story_v2.
Este script reutiliza as funções dele para medir a v1 e preencher a tabela comparativa do README.

Uso: python src/evaluate_baseline.py
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client

import evaluate as ev

load_dotenv()


def main():
    ev.print_section_header("AVALIAÇÃO DO PROMPT BASELINE (v1)")
    if not ev.check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB", "LLM_PROVIDER"]):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    project_name = os.getenv("LANGSMITH_PROJECT", "prompt-optimization-challenge-resolved")
    dataset_name = f"{project_name}-eval"

    client = Client()
    ev.create_evaluation_dataset(client, dataset_name, "datasets/bug_to_user_story.jsonl")

    prompt_name = f"{username}/bug_to_user_story_v1"
    scores = ev.evaluate_prompt(prompt_name, dataset_name, client)
    passed = ev.display_results(prompt_name, scores)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
