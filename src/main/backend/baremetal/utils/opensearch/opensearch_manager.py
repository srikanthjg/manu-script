# scripts/opensearch_manager.py
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth, NotFoundError
from utils.config import OPENSEARCH_HOST, OPENSEARCH_PORT, OPENSEARCH_USER, OPENSEARCH_PASSWORD, REGION
import boto3 

# Define the settings and mappings
INDEX_MAPPINGS_SETTINGS = {
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 0
    }
  },
  "mappings": {
    "properties": {
      "chunk_content": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "chunk_metadata": {
        "properties": {
          "chunk_index": {
            "type": "long"
          },
          "document_id": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "roles": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      },
      "chunk_vector_field": {
        "type": "knn_vector",
        "dimension": 1536,
        "method": {
          "engine": "nmslib",
          "space_type": "cosinesimil",
          "name": "hnsw",
          "parameters": {}
        }
      }
    }
  }
}


class OpenSearchClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenSearchClient, cls).__new__(cls)
            service = 'aoss'
            credentials = boto3.Session().get_credentials()
            auth = AWSV4SignerAuth(credentials, REGION, service)
            cls._instance.client = OpenSearch(
                hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
                http_auth=auth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                pool_maxsize=20,
            )
        return cls._instance

    def get_client(self):
        return self.client

    def create_index(self, index_name, settings=None, mappings=None):
        client = self.get_client()
        body = {}
        if settings:
            body['settings'] = settings
        if mappings:
            body['mappings'] = mappings

        response = client.indices.create(index=index_name, body=body)
        return response

    def delete_index(self, index_name):
        client = self.get_client()
        response = client.indices.delete(index=index_name)
        return response

    def list_indices(self):
        client = self.get_client()
        response = client.cat.indices(format='json')
        return response

    def index_exists(self, index_name):
        client = self.get_client()
        return client.indices.exists(index=index_name)
    
    def search(self, index):
        client = self.get_client()
        return client.search(index)