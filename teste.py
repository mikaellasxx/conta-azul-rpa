from dotenv import load_dotenv
from services.auth import get_access_token
import os

load_dotenv()
tokens = get_access_token()
print(tokens["access_token"])
