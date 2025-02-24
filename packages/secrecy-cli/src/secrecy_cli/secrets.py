from secrecy import Secret, register_source
from todo_replace_me import foobar

# TODO: Link to the relevant docs
register_source("default", foobar, default=True)

# These for demonstration purposes only. Feel free to replace them with your own secrets.
api_token = Secret("api_token")
db_credentials = Secret("db_credentials")

# To use these,
