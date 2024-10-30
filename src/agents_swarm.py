from swarm import Template, SwarmAPI
import os
import pandas as pd


def load_prompt_template(prompt_path: str):
    """
    Load a prompt template from a file path.

    Args:
        prompt_path (str): Path to the prompt file.

    Returns:
        PromptTemplate: The loaded prompt template.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    if not os.path.isfile(prompt_path):
        raise FileNotFoundError(f"Prompt file '{prompt_path}' does not exist.")

    with open(prompt_path, 'r', encoding='utf-8') as file:
        markdown_string = file.read()
    return Template(markdown_string)


def finance_data_analyst(data: pd.DataFrame, prompt):
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Provided data must be a pandas DataFrame.")

    prompt_template = load_prompt_template(prompt)
    return prompt_template.render(data)