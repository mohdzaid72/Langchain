from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field



load_dotenv()



llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation"
    
)
model=ChatHuggingFace(llm=llm)

class Perosn(BaseModel):
    name: str = Field(description="name of the person")
    age: int = Field(gt=18,description = 'Age of the person')
    city: str = Field (description='living city of the person')

parser=PydanticOutputParser(pydantic_object=Perosn)

temp=PromptTemplate(
    template='generate 3 name , age and city of the frictional {place} persone\n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

prompt=temp.invoke({'place':'india'})
result=model.invoke(prompt)
final_res=parser.parse(result.content)
print(final_res)

