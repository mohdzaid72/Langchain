from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import PromptTemplate

st.header('Research Tool')
st.write('This tool is used to answer questions related to research.')
#querry=st.text_input("Enter your query here:")

paper_input = st.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

temp=PromptTemplate(
    template=""" Please summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}  
Explanation Length: {length_input}  
1. Mathematical Details:  
   - Include relevant mathematical equations if present in the paper.  
   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.  
2. Analogies:  
   - Use relatable analogies to simplify complex ideas.  
If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.  
Ensure the summary is clear, accurate, and aligned with the provided style and length. """,
 input_variables=["paper_input", "style_input", "length_input"],
 validate_template=True   
)
#filling the placeholders with user inputs
querry=temp.format(   #if when we are working with langchain closed source models, we need to use format instead of invoke. both have different syntax
    paper_input=paper_input,
    style_input=style_input,
    length_input=length_input
)




llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)  # Initialize the Hugging Face model endpoint
llm.temperature = 1  # Set the temperature for the model


model = ChatHuggingFace(llm=llm)  # Initialize the chat model
#print(model.model)  # Print the model details
result=model.invoke(querry) # Invoke the model with the formatted query
if st.button("analyze"):
    st.write(result.content)  # Display the result in the Streamlit app