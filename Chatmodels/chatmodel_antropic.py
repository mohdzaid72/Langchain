form langchain_antropic import ChatAnthropic
from dotenv import load_dotenv
load_dotenv()

model=ChatAnthropic(model="claude-2", temperature=0.7)  # Initialize the chat model
result = model.invoke("What is the capital of France?")  # Example usage
print(result.content)  # Print the response from the model