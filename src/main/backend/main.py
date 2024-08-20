# main.py
import os
import json

# from utils.file_manager import FileManager
from utils.iam_manager import IAMManager
from utils.opensearch.opensearch_manager import OpenSearchClient,INDEX_MAPPINGS_SETTINGS
from utils.retriever import Retriever, RoleBasedSimilarityRetrieval
from utils.ingestion import ingest_to_vectordb
from utils.chunker import FileChunker
from langchain.text_splitter import RecursiveCharacterTextSplitter


def main():
    # Initialize components
    allowed_roles = ['arn:aws:iam::176893235612:role/Admin', 'arn:aws:iam::176893235612:role/aos-ingestion-role']    
    file_path = os.path.join('src/main/backend/data/essay.txt')
    index_name = "parent_child_doc_chunks"
    
    # Chunk
    #File Chunker also holds all data and chunks metadata
    chunker = FileChunker(RecursiveCharacterTextSplitter(chunk_size=10,
                                    chunk_overlap=0), allowed_roles)
    chunks_data, chunk_ids = chunker.process_file(file_path)
    print("Chunks:")
    print(chunker.document_metadata)  
    
    #Upload to VectorDB - opensearch
    ingest_to_vectordb( index_name, chunks_data, chunk_ids)

    # # Retrieve chunks based on IAM role and similarity search
    # retriever = Retriever(RoleBasedSimilarityRetrieval())
    
    # #Retreive
    # user_role = 'arn:aws:iam::176893235612:role/Admin'
    # print("Enter query in the form of opensearch DSL:")
    # query = input()
    # try:
    #     retrieved_chunks = retriever.retrieve(query, index_name, user_role)
    #     for chunk in retrieved_chunks:
    #         print(chunk['_source'])
    # except PermissionError as e:
    #     print(e)


if __name__ == "__main__":
    main()
