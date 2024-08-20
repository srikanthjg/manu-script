# scripts/chunker.py
import os
import json
import uuid

# Define the chunk size and overlap
CHUNK_SIZE = 1000  # Adjust as needed
CHUNK_OVERLAP = 200  # Adjust as needed

class FileChunker:
    def __init__(self, chunker, roles):
        self.chunker = chunker
        self.roles = roles
        self.document_metadata = {} #id: #roles:str ,chunk_ids:list
        self.chunks_metadata = {} # id: #doc_id:int , chunk_index:int, roles:str 

    def chunk_file(self, file_path):
        content=""
        with open(file_path, 'r') as file:
            content = file.read()
        chunks = self.chunker.split_text(content)
        return chunks, content

    def save_chunks_meta_data(self, document_id, chunks):
        chunks_data = {}
        chunk_ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            if chunk_id not in chunks_data:
                chunks_data[chunk_id] = {}
            chunks_data[chunk_id]["content"] = chunk
            chunks_data[chunk_id]["metadata"] = {
                'document_id': document_id,
                'chunk_index': i,
                'roles': self.roles
            }
            chunk_ids.append(chunk_id)
            self.chunks_metadata[chunk_id] = chunks_data
        return chunks_data, chunk_ids

    def process_file(self, file_path:str):
        #TODO - check for duplicates
        
        #Get chunks and its metadata
        document_id = str(uuid.uuid4())
        chunks, file_content = self.chunk_file(file_path)
        chunks_data, chunk_ids = self.save_chunks_meta_data(document_id, chunks)

        #update parent doc metadata
        file_name = file_path.split("/")[-1]
        
        self.document_metadata[document_id] = {
            'chunk_ids': chunk_ids,
            'roles': self.roles
        }
    
        return chunks_data, chunk_ids 