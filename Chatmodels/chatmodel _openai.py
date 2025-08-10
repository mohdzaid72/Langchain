from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
model=ChatOpenAI(models="gpt-4", temperature=0.7,max_completiom_tokens=10)  # Initialize the chat model
result =model.invoke("What is the capital of France?")  # Example usage
print(result.content)  # Print the response from the model
   