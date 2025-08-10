from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)
model=ChatHuggingFace(llm=llm)

temp1= PromptTemplate(
    template="Explain the {topic} in detail",
    input_variables=['topic']
)

temp2= PromptTemplate(
    template="write the 5 line summary in the following text\n {text}",
    input_variables=['text']
)
parser=StrOutputParser()

chain= temp1|model|parser|temp2|model|parser

print(chain.invoke({'topic':'black hole'}))