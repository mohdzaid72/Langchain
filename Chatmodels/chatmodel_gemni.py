from lancchain_gemni import ChatGemini
from dotenv import load_dotenv
load_dotenv()

model=ChatGimini(model="gemini-1.5-flash", temperature=0.7)  # Initialize the chat model
model.invoke("What is the capital of France?")  # Example usage
print(model.content)  # Print the response from the model