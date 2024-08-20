from utils.opensearch.opensearch_manager import NotFoundError
from utils.bedrock import Bedrock
from utils.opensearch.opensearch_manager import OpenSearchClient,INDEX_MAPPINGS_SETTINGS

def ingest_to_vectordb(index_name, chunks_data, chunk_ids):
    client = OpenSearchClient().get_client()
    # Check if the index already exists
    try:
        if not client.indices.exists(index=index_name):
            # Create the index if it does not exist
            response = client.indices.create(index=index_name, body=INDEX_MAPPINGS_SETTINGS)
            print(f"Index '{index_name}' created:", response)
        else:
            print(f"Index '{index_name}' already exists. Skipping creation.")
    except NotFoundError as e:
        print(f"Error occurred: {e}")

    try: 
        # Upload to OpenSearch
        upload_to_opensearch(client, index_name, chunks_data, chunk_ids)
        print("Data uploaded to OpenSearch index successfully.")
        return True
    except Exception as e:
        print(f"Error uploading data to OpenSearch: {e}")
        
    
def upload_to_opensearch(client, index_name, chunks_data, chunk_ids):
    for chunk_id in chunk_ids:
        _chunk = {
            'chunk_content': chunks_data[chunk_id]['content'],
            'chunk_metadata': chunks_data[chunk_id]['metadata'],
            'chunk_vector_field' : Bedrock().get_embedding(chunks_data[chunk_id]['content'])
        }
        #print("uploading {} to index {}",_chunk,index_name)
        client.index(index=index_name, body=_chunk)