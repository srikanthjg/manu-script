# scripts/iam_manager.py
import boto3
import os
from botocore.exceptions import ClientError

class AccessDeniedException(Exception):
    """Custom exception to be thrown when access is denied."""
    pass

class IAMManager:
    def __init__(self):
        self.iam_client = boto3.client('iam')

    def is_role_allowed(self, role):
        try:
            self.iam_client.get_role(RoleName=role)
            return True
        except self.iam_client.exceptions.NoSuchEntityException:
            return False
        
    def assume_role(role_arn, session_name="default-session"):
        sts_client = boto3.client('sts')
        try:
            assumed_role = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName=session_name
            )
            credentials = assumed_role['Credentials']
            return credentials
        except ClientError as e:
            raise AccessDeniedException(f"Access denied when assuming role: {str(e)}")

    def associate_role_with_chunks(self, file_name, roles):
        for role in roles:
            if self.assume_role(role) or self.assume_role(role):
                role_dir = os.path.join('iam_roles', role)
                os.makedirs(role_dir, exist_ok=True)
                chunks_dir = os.path.join('chunks', file_name)
                if os.path.exists(chunks_dir):
                    for chunk in os.listdir(chunks_dir):
                        chunk_path = os.path.join(chunks_dir, chunk)
                        role_file_path = os.path.join(role_dir, f'{file_name}_{chunk}')
                        with open(role_file_path, 'w') as role_file:
                            role_file.write(chunk_path)
            else:
                print(f"Role {role} is not allowed.")
