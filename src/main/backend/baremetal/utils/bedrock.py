import boto3
import json

LLM_AMZN_TITAN_EMBEDDING_MODEL =  "amazon.titan-embed-text-v1"
class Bedrock():
    def __init__(self):
        self.client = boto3.client('bedrock-runtime',region_name='us-east-1')

    def invoke_llm(self,model, prompt):
        body={
            "prompt": prompt,
            "max_tokens_to_sample": 300,
            "temperature": 0.5,
            "top_k": 250,
            "top_p": 1,
            "stop_sequences": [
                "\n\nHuman:"
            ],
            "anthropic_version": "bedrock-2023-05-31"
        }

        response = self.client.invoke_model(
            body=json.dumps(body),
            contentType='application/json',
            accept="*/*",
            modelId=model
        )
        response_body = json.loads(response["body"].read())
        print(response)
        print(response_body['completion'])
        
    def get_embedding(self, data):
        body = json.dumps({"inputText": data})
        modelId =  LLM_AMZN_TITAN_EMBEDDING_MODEL # (Change this to try different embedding models)
        accept = "application/json"
        contentType = "application/json"

        response = self.client.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())

        embedding = response_body.get("embedding")
        return embedding
        