

import requests
from dotenv import load_dotenv
import os
import base64

authorization_url = "https://auth.contaazul.com/oauth2/token"

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")  
refresh_token = os.getenv("REFRESH_TOKEN")

def update_refresh_token(new_refresh_token):
    with open(".env", "r") as file:
        lines = file.readlines()

    with open(".env", "w") as file:
        for line in lines:
            if line.startswith("REFRESH_TOKEN="):
                file.write(f"REFRESH_TOKEN={new_refresh_token}\n")
            else:
                file.write(line)

def get_access_token():
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(authorization_url, headers=headers, data=data)    

    tokens = response.json()

    if "refresh_token" in tokens:
        update_refresh_token(tokens["refresh_token"])


    return tokens   

