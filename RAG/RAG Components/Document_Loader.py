from langchain_community.document_loaders import TextLoader,PyPDFLoader,DirectoryLoader, WebBaseLoader


#Use of text Loader 
"""loader=TextLoader("Sample.txt",encoding="latin-1")

docs = list(loader.lazy_load())  # convert generator to list
print(docs[0]) 

"""

#use of pdf loader

"""loader=PyPDFLoader('Zaid Resume.pdf')
doc=loader.load()
print(doc[0])
"""


#using directory loader
"""loader=DirectoryLoader(
    path='RAG Components',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)
doc=loader.load()
print(doc[0].page_content)
 """
# using WebBaseLoader 

url="https://en.wikipedia.org/wiki/Main_Page"
loader=WebBaseLoader(url)

doc=loader.load()
print(doc[0].page_content)