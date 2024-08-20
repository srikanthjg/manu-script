from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# from data.data import essay

loader = TextLoader("./data/essay.txt")
docs = []
docs.extend(loader.load())

print(docs)    
#[Document(metadata={'source': './data/paul_graham_essay.txt'}, page_content='Do Things...'ll keep doing it when you have a lot.\n')]

# This text splitter is used to create the child documents
child_splitter = RecursiveCharacterTextSplitter(chunk_size=10,chunk_overlap=0)
# The vectorstore to use to index the child chunks
vectorstore = Chroma(
    collection_name="full_documents", embedding_function=OpenAIEmbeddings() 
)

# The storage layer for the parent documents
store = InMemoryStore() # stores as key value pair in memory
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter, #chunking strategy
)
#add all doc into vectorDB
retriever.add_documents(docs, ids=None)




# list(store.yield_keys())
# sub_docs = vectorstore.similarity_search("cc")
# print(sub_docs[0].page_content)


retrieved_docs = retriever.invoke("cc")
len(retrieved_docs[0].page_content)
print(retrieved_docs[0].page_content)