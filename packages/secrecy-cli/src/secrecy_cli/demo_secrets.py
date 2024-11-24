# from secrecy.builder import Environment
from secrecy_file.sources.encrypted_file.sync import EncryptedFiles

# A builder, that is scoped to the source.
source = EncryptedFiles("secrets")

# It can build secret definitions attached to the source, which share
# credentials, defaults, etc.
sample_secret = source.secret("sample")
db_credentials = source.secret("db_credentials")

# from_env = Environment.secret("from_env")
# _also_ignored = Environment.async_secret("also_ignored")
