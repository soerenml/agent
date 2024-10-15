from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import pandas as pd
import os


def finance_data_analyst(prompt: str, data: pd.DataFrame, llm: ChatOpenAI):
    """
    Analyzes financial data using a prompt and a language model.

    Args:
        prompt (str): The path to the file containing the prompt for analysis.
        data (pandas.DataFrame): The financial data to be analyzed.
        llm (ChatOpenAI): The language model used for analysis.

    Returns:
        str: The result of the analysis.

    Raises:
        ValueError: If the provided data is not a pandas DataFrame.
        FileNotFoundError: If the prompt file does not exist.

    """
    # Validate input parameters
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Provided data must be a pandas DataFrame.")

    if not os.path.isfile(prompt):
        raise FileNotFoundError(f"Prompt file '{prompt}' does not exist.")

    with open(prompt, 'r', encoding='utf-8') as file:
        markdown_string = file.read()

    prompt_custom = PromptTemplate.from_template(markdown_string)

    rag_chain = (
        {"data": RunnablePassthrough()}
        | prompt_custom
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke({"data": data})


def finance_news_analyst(prompt: str, all_headlines: list, llm: ChatOpenAI):
    """
    Analyzes financial news using a language model.

    Args:
        prompt (str): The path to the file containing the prompt template.
        all_headlines (list): A list of headlines to be used as input for the analysis.
        llm (ChatOpenAI): The language model used for generating responses.

    Returns:
        dict: The result of the analysis.

    Raises:
        ValueError: If the provided data is not a string.
        FileNotFoundError: If the file specified by the `prompt` parameter does not exist.
    """
    # Validate input parameters
    if not isinstance(prompt, str):
        raise ValueError("Provided data must be a string.")

    if not os.path.isfile(prompt):
        raise FileNotFoundError(f"Prompt file '{prompt}' does not exist.")

    with open(prompt, 'r', encoding='utf-8') as file:
        markdown_string = file.read()

    prompt_custom = PromptTemplate.from_template(markdown_string)

    rag_chain = (
        {"headlines": RunnablePassthrough()}
        | prompt_custom
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke({"headlines": all_headlines})


def head_analyst(prompt: str, result_1: str, result_2: str, llm: ChatOpenAI):
    """
    Perform analysis using the provided prompt, result_1, result_2, and llm.

    Args:
        prompt (str): The path to the prompt file or the prompt string itself.
        result_1 (str): The first result string.
        result_2 (str): The second result string.
        llm (ChatOpenAI): The ChatOpenAI object used for language model interaction.

    Raises:
        ValueError: If the provided prompt is not a string.
        FileNotFoundError: If the prompt file does not exist.

    Returns:
        dict: The final result of the analysis.
    """

    # Validate input parameters
    if not isinstance(prompt, str):
        raise ValueError("Provided data must be a string.")

    if not os.path.isfile(prompt):
        raise FileNotFoundError(f"Prompt file '{prompt}' does not exist.")
    with open(prompt, 'r', encoding='utf-8') as file:
        markdown_string = file.read()

    prompt_custom = PromptTemplate.from_template(markdown_string)

    rag_chain = (
        {"string_1": RunnablePassthrough(), "string_2": RunnablePassthrough(), "string_3": RunnablePassthrough()}
        | prompt_custom
        | llm
        | StrOutputParser()
    )
    final_result = rag_chain.invoke({"string_1": result_1, "string_2": result_2})

    return final_result
