from langchain.text_splitter import CharacterTextSplitter , RecursiveCharacterTextSplitter , Language
from langchain_community.document_loaders import PyPDFLoader


#document loader
loader=PyPDFLoader('Zaid Resume.pdf')
docs=loader.load()

#length based text splotter
"""splitter=CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=2,
    separator=""
)
split_docs=splitter.split_documents(docs) # i return list 
#fot single text file: use - split_text("text")
print(split_docs[0].page_content)

"""

#Text structured bsed Splitter


text="""My name is nitesh
i am 35 years old

i live in gurgaon"""

"""
splitter=RecursiveCharacterTextSplitter(
    chunk_size=10,
    chunk_overlap=0
)
splited_text=splitter.split_text(text)
print(splited_text)

"""
#Document Structure based splitter


code="""
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade  # Grade is a float (like 8.5 or 9.2)

    def get_details(self):
        return self.name"

    def is_passing(self):
        return self.grade >= 6.0


# Example usage
student1 = Student("Aarav", 20, 8.2)
print(student1.get_details())

if student1.is_passing():
    print("The student is passing.")
else:
    print("The student is not passing.")
"""
splitter= RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=75,
    chunk_overlap=0
)

splitted_code=splitter.split_text(code)
print(splitted_code)