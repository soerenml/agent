from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import pandas as pd
import os


def load_prompt_template(prompt_path: str) -> PromptTemplate:
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
    return PromptTemplate.from_template(markdown_string)


def invoke_chain(prompt_template: PromptTemplate, llm: ChatOpenAI, inputs: dict):
    """
    Invoke the RAG chain with the given inputs.

    Args:
        prompt_template (PromptTemplate): The prompt template for the chain.
        llm (ChatOpenAI): The language model for the chain.
        inputs (dict): The input data for invocation.

    Returns:
        The result of the chain invocation.
    """
    rag_chain = prompt_template | llm | StrOutputParser()
    return rag_chain.invoke(inputs)


def finance_data_analyst(prompt: str, data: pd.DataFrame, asset: str, llm: ChatOpenAI):
    """
    Analyzes financial data using a prompt and a language model.

    Args:
        prompt (str): The path to the file containing the prompt for analysis.
        data (pandas.DataFrame): The financial data to be analyzed.
        asset (str): The asset to be analyzed.
        llm (ChatOpenAI): The language model used for analysis.

    Returns:
        str: The result of the analysis.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Provided data must be a pandas DataFrame.")

    prompt_template = load_prompt_template(prompt)
    return invoke_chain(prompt_template, llm, {"data": data, "asset": asset})


def finance_news_analyst(prompt: str, all_headlines: list, llm: ChatOpenAI):
    """
    Analyzes financial news using a language model.

    Args:
        prompt (str): The path to the file containing the prompt template.
        all_headlines (list): A list of headlines to be used as input for the analysis.
        llm (ChatOpenAI): The language model used for generating responses.

    Returns:
        dict: The result of the analysis.
    """
    if not isinstance(all_headlines, list):
        raise ValueError("Provided headlines must be a list.")

    prompt_template = load_prompt_template(prompt)
    return invoke_chain(prompt_template, llm, {"headlines": all_headlines})


def head_analyst(prompt: str, result_1: str, result_2: str, result_3: str, llm: ChatOpenAI):
    """
    Perform analysis using the provided prompt, result_1, result_2, and llm.

    Args:
        prompt (str): The path to the prompt file or the prompt string itself.
        result_1 (str): The first result string.
        result_2 (str): The second result string.
        llm (ChatOpenAI): The ChatOpenAI object used for language model interaction.

    Returns:
        dict: The final result of the analysis.
    """
    prompt_template = load_prompt_template(prompt)
    return invoke_chain(prompt_template, llm, {"string_1": result_1, "string_2": result_2, "string_3": result_3})


def technical_data_analyst(prompt: str, data: pd.DataFrame, asset: str, llm: ChatOpenAI):
    """
    Analyzes technical financial data using a prompt and a language model.

    Args:
        prompt (str): The path to the file containing the prompt for analysis.
        data (pandas.DataFrame): The technical financial data to be analyzed.
        asset (str): The asset to be analyzed.
        llm (ChatOpenAI): The language model used for analysis.

    Returns:
        str: The result of the analysis.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Provided data must be a pandas DataFrame.")

    prompt_template = load_prompt_template(prompt)
    return invoke_chain(prompt_template, llm, {"data": data, "asset": asset})
