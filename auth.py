from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

# in production, we get this value from .env
load_dotenv()

# call api_key from .env file
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key:str = Header()):
    """Verify the API key from the request header"""

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
