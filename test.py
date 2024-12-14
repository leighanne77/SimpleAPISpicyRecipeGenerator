import os
print("Starting script...")
from dotenv import load_dotenv
print("Loaded dotenv...")
load_dotenv()
print(f"API Key: {os.getenv('SPOONACULAR_API_KEY')}")
