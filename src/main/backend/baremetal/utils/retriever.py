# scripts/retriever.py
import json
from utils.opensearch.opensearch_manager import OpenSearchClient # type: ignore
from utils.iam_manager import IAMManager

class RetrievalStrategy:
    def retrieve_chunks(self, query, role):
        raise NotImplementedError

class RoleBasedSimilarityRetrieval(RetrievalStrategy):
    def __init__(self):
        self.iam_manager = IAMManager()

    def retrieve_chunks(self, query, index_name, role):
        if not self.iam_manager.is_role_allowed(role):
            raise PermissionError(f"Role {role} is not allowed.")

        client = OpenSearchClient().get_client()
        # vector_query = {
        #     "size": 10,
        #     "query": {
        #         "bool": {
        #             "must": [
        #                 {
        #                     "match": {
        #                         "roles": role
        #                     }
        #                 },
        #                 {
        #                     "script_score": {
        #                         "query": {
        #                             "match_all": {}
        #                         },
        #                         "script": {
        #                             "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
        #                             "params": {
        #                                 "query_vector": query
        #                             }
        #                         }
        #                     }
        #                 }
        #             ]
        #         }
        #     }
        # }
        response = client.search(index=index_name, body=query)
        return response['hits']['hits']

class Retriever:
    def __init__(self, strategy: RetrievalStrategy):
        self.strategy = strategy

    def retrieve(self, query, index_name, role):
        return self.strategy.retrieve_chunks(query, index_name, role)
