from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3

host = 'g33jzziefmc977bz6w4i.us-east-1.aoss.amazonaws.com'  # serverless collection endpoint, without https://
region = 'us-east-1'  # e.g. us-east-1

service = 'aoss'
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, region, service)

# create an opensearch client and use the request-signer
client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    pool_maxsize=20,
)

# # create an index
# index_name = 'books-index'
# create_response = client.indices.create(
#     index_name
# )

# print('\nCreating index:')
# print(create_response)

# create an index for a document
# document = {
#   'title': 'The Green Mile',
#   'director': 'Stephen King',
#   'year': '1996'
# }

# response = client.index(
#     index = 'books-index',
#     body = document
#     # id = '1'
# )
# print(response)


#get a document
response = client.search(index="books-index")
print("search output:")
print(response)
# # delete the index
# delete_response = client.indices.delete(
#     index_name
# )

# print('\nDeleting index:')
# print(delete_response)