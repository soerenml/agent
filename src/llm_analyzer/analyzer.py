from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

def llm_analyzer(prompt: str, all_headlines: list, llm: ChatOpenAI):

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