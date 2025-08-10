#closed source API code
from langchain_openai import OpenAI
from dotvenv import load_dontenv

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo", temperature=0.7)    
print("LLM initialized with model:", llm.model)
genres=llm.generate("What is the capital of France?")  # Example usage
invres=llm.invoke("What is the capital of France?")  # Example usage
print("Response from generate:", genres)
#no need to print result .content because it take string as input and output.
print("Response from invoke:", invres)
