from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from langchain.schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda



load_dotenv()

parser=StrOutputParser() # last me string me output lene ke liyen

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation"
)
model=ChatHuggingFace(llm=llm)


class Review(BaseModel):
    sentiment:Literal['Positive','Negative']=Field(description='give sentiment of the review')
    
parser2=PydanticOutputParser(pydantic_object=Review)  # kyunki type ki restrict krna tha and sentiment words ko bhi

temp1=PromptTemplate(
    template='Classify the sentiment of the following feedback text into postive or negative \n {review} \n {format_instruction}',
    input_variables=['review'],
    partial_variables={'format_instruction':parser2.get_format_instructions()}
)

classifier_chain= temp1|model|parser2  #tell semtiment positive h ya negative

temp2=PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {review}',
    input_variables=['review']
)


temp3=PromptTemplate(
    template='Write an appropriate response to this negative feedback \n {review}',
    input_variables=['review']
)

conditional_branch=RunnableBranch(
    (lambda x:x.sentiment=='Positive',temp2|model|parser),
    (lambda x:x.sentiment=='Negative',temp3|model|parser),
    RunnableLambda(lambda x: "could not find sentiment")

)
 
chain=classifier_chain|conditional_branch
print(chain.invoke({'review': 'this is a rubish phone'}))