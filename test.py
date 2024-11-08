import os
from dotenv import load_dotenv

load_dotenv()
print(f"API Key: {os.getenv('SPOONACULAR_API_KEY')}")