from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from dotenv import load_dotenv

load_dotenv()
llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="question-answering"    
)
chat_history=[SystemMessage(content="You are a helpful assistant.")]

model=ChatHuggingFace(llm=llm)
while True:
    question=input("user:")
    chat_history.append(HumanMessage(content=question))
    
    
    if question.lower() == 'exit':       
    
        print("Exiting the chatbot.")
        break
    print('user:'+question)

    answer=model.invoke(chat_history)  # Invoke the model with the chat history
    chat_history.append(AIMessage(content=answer.content))  

    print('AI:'+answer.content)



