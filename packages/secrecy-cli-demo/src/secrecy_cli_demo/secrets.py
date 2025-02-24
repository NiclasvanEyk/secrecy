from pydantic import BaseModel
from secrecy import Secret, register_source
from secrecy_aws.boto3 import SecretsManagerSource


class DatabaseCredentials(BaseModel):
    protocol: str
    host: str
    user: str
    password: str
    port: int


register_source("aws", SecretsManagerSource, default=True)

db_credentials = Secret("db_credentials", shape=DatabaseCredentials)
api_token = Secret("api_token")
oauth_tokens = Secret("oauth_tokens", dict[str, str])
another_api_token = Secret("another_api_token")
