import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1 - Invoke the model
print(llm.invoke("how can langsmith help with testing?"))

# 2 - Chains
# 2.1 - Use a prompt template
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])

# 2.2 - (Optional) Output parser
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

# 2.3 - Chain the components
chain = prompt | llm | output_parser
print(chain.invoke({"input": "how can langsmith help with testing?"}))