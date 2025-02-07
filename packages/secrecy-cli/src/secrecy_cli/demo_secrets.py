# from secrecy.builder import Environment
from secrecy.sources.dynamic.sync import EnvironmentConfiguredSecrets
from secrecy_file.sources.encrypted_file.sync import EncryptedFiles

# A builder, that is scoped to the source.
files = EncryptedFiles("secrets")

dynamic = EnvironmentConfiguredSecrets(driver=env("FOOBAR", "file"))

# It can build secret definitions attached to the source, which share
# credentials, defaults, etc.
sample_secret = files.secret("sample")
db_credentials = files.secret("db_credentials")

# from_env = Environment.secret("from_env")
# _also_ignored = Environment.async_secret("also_ignored")
