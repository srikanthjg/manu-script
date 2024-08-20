import boto3
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import OpenSearchVectorStore
from opensearchpy import OpenSearch,AWSV4SignerAuth
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = "your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-access-key"
AWS_REGION = 'us-east-1'  
OPENSEARCH_ENDPOINT = "g33jzziefmc977bz6w4i.us-east-1.aoss.amazonaws.com"
INDEX_NAME = "your-index-name"
OPENAI_API_KEY = "your-openai-api-key"
IAM_ROLE_ARN = "arn:aws:iam::your-account-id:role/your-role-name"
SERVICE = 'aoss'
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, AWS_REGION, SERVICE)

# Initialize the AWS STS client to assume roles
sts_client = boto3.client(
    'sts',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# Initialize the OpenSearch client
opensearch_client = OpenSearch(
    hosts=[{'host': OPENSEARCH_ENDPOINT, 'port': 443}],
    http_compress=True,
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

# Initialize the vector database with OpenAI embeddings
vectordb = OpenSearchVectorStore(
    client=opensearch_client,
    index_name=INDEX_NAME,
    embedding_model=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
)

# Function to convert PDF to text and chunk it
def pdf_to_chunks(pdf_path, iam_role_arn):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # Add IAM role to metadata of each chunk
    for chunk in chunks:
        chunk.metadata["iam_role_arn"] = iam_role_arn

    return chunks

# Function to add a document to the vector database
def add_document_to_vectordb(pdf_path, iam_role_arn):
    chunks = pdf_to_chunks(pdf_path, iam_role_arn)
    vectordb.add_documents(chunks)
    print(f"Added {len(chunks)} chunks to the vector database with IAM role {iam_role_arn}.")

# Function to check if the user can assume the role
def assume_role(role_arn):
    try:
        sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="langchain_session"
        )
        print(f"Assumed role {role_arn} successfully.")
        return True
    except ClientError as e:
        print(f"Error assuming role {role_arn}: {str(e)}")
        return False

# Function to retrieve documents with role validation
def retrieve_documents_with_role_validation(query, user_role_arn):
    # Perform a search query on OpenSearch
    results = vectordb.search(query)
    
    # Filter results based on role validation
    valid_chunks = []
    for result in results:
        chunk = result['document']
        required_role = chunk.metadata.get("iam_role_arn")
        
        if required_role and assume_role(required_role):
            valid_chunks.append(chunk)
        else:
            print(f"User role {user_role_arn} is not authorized to access this chunk.")
    
    return valid_chunks

if __name__ == "__main__":
    # Path to your local PDF file
    local_pdf_path = "document.pdf"

    # Add the document to the vector database with an IAM role
    add_document_to_vectordb(local_pdf_path, IAM_ROLE_ARN)

    # Perform a query and retrieve documents with role validation
    user_query = "your search query"
    user_role_arn = "arn:aws:iam::your-account-id:role/user-role"
    retrieved_chunks = retrieve_documents_with_role_validation(user_query, user_role_arn)
    
    print(f"Retrieved {len(retrieved_chunks)} chunks that the user is authorized to access.")
