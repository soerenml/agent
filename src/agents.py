from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import pandas


def finance_data_analyst(prompt: str, data: pandas.DataFrame, llm: ChatOpenAI):
    """
    Analyzes financial data using a prompt and a language model.

    Args:
        prompt (str): The path to the file containing the prompt for analysis.
        data (pandas.DataFrame): The financial data to be analyzed.
        llm (ChatOpenAI): The language model used for analysis.

    Returns:
        str: The result of the analysis.

    Raises:
        FileNotFoundError: If the prompt file does not exist.

    """
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
        FileNotFoundError: If the file specified by the `prompt` parameter does not exist.
    """
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