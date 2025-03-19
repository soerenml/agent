from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import pandas as pd
import os
from datetime import datetime


def run_llm(
        prompt_path: str,
        llm: ChatOpenAI,
        inputs: dict,
        print_prompt: bool = False):

    if not os.path.isfile(prompt_path):
        raise FileNotFoundError(f"Prompt file '{prompt_path}' does not exist.")

    with open(prompt_path, 'r', encoding='utf-8') as file:
        markdown_string = file.read()

    prompt_template = PromptTemplate.from_template(markdown_string)

    if print_prompt:
        rendered_prompt = prompt_template.format(**inputs)
        print("\n===========================\n")
        print(rendered_prompt)
        print("\n===========================\n")

    rag_chain = prompt_template | llm | StrOutputParser()
    llm_output = rag_chain.invoke(inputs)

    return llm_output


def summerize_agent(
        prompt_path: str,
        data: str,
        llm: ChatOpenAI):
    """
    Summarizes the provided data using a prompt and a language model.

    Args:
        prompt (str): The path to the file containing the prompt for analysis.
        data (str): The text data to be analyzed.
        asset (str): The asset to be analyzed.
        llm (ChatOpenAI): The language model used for analysis.

    Returns:
        str: The result of the analysis.
    """
    if not isinstance(data, str):
        raise ValueError("Provided data must be a pandas DataFrame.")

    llm_output = run_llm(
        prompt_path=prompt_path,
        llm=llm,
        inputs={"data": data})

    return llm_output


def finance_data_analyst(
        prompt_path: str,
        data: pd.DataFrame,
        asset: str,
        llm: ChatOpenAI):
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

    llm_output = run_llm(
        prompt_path=prompt_path,
        llm=llm,
        inputs={"data": data, "asset": asset})

    return llm_output


def finance_news_analyst(
        prompt_path: str,
        all_headlines: list,
        llm: ChatOpenAI):
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

    llm_output = run_llm(
        prompt_path=prompt_path,
        llm=llm,
        inputs={"headlines": all_headlines})

    return llm_output


def technical_data_analyst(
        prompt_path: str,
        data: pd.DataFrame,
        asset: str,
        llm: ChatOpenAI):
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

    llm_output = run_llm(
        prompt_path=prompt_path,
        llm=llm,
        inputs={"data": data, "asset": asset})

    return llm_output


def head_analyst(
        prompt_path: str,
        result_news_analyst: str,
        result_finance_analyst: str,
        result_technical_analyst: str,
        llm: ChatOpenAI,
        date: datetime,
        historical_data: str,
        missed_strong_sell: str,
        missed_strong_buy: str,
        print_prompt: bool = False):
    """
    Perform analysis using the provided prompt, results, and LLM.

    Args:
        prompt (str): The path to the prompt file or the prompt string itself.
        result_1 (str): The first result string.
        result_2 (str): The second result string.
        result_3 (str): The third result string.
        llm (ChatOpenAI): The ChatOpenAI object used for language model interaction.
        date (datetime): The current date to include in the analysis.
        historical_data (str): Historical data for analysis.
        missed_strong_sell (str): Where agent should have sold but missed.
        missed_strong_buy (str): Where agent should have bought but missed.

    Returns:
        dict: The final result of the analysis.
    """
    inputs = {
        "result_news_analyst": result_news_analyst,
        "result_finance_analyst": result_finance_analyst,
        "result_technical_analyst": result_technical_analyst,
        "date": date,
        "historical_data": historical_data,
        "missed_strong_sell": missed_strong_sell,
        "missed_strong_buy": missed_strong_buy
    }


    llm_output = run_llm(
        prompt_path=prompt_path,
        llm=llm,
        inputs=inputs,
        print_prompt=print_prompt)

    return llm_output