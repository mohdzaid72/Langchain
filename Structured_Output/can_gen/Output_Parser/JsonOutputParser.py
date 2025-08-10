from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()
parser=JsonOutputParser()

temp=PromptTemplate(
    template='tell me the datail about five frictional persons including their name, city, profession \n {format_instructions}',
    #input_variables=[],
    partial_variables={'format_instructions': parser.get_format_instructions()}
    
)

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    task="text-generation"
)

model=ChatHuggingFace(llm=llm)

"""prompt=temp.invoke({})
result=model.invoke(prompt).content
final_res=parser.parse(result)
"""
chain= temp|model|parser
final_res=chain.invoke({})

print(final_res)

