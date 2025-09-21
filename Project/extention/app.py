llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    temperature=1,
    max_new_tokens=512
)

model = ChatHuggingFace(llm=llm)

response = model.invoke(input_text)
print(response.content)
