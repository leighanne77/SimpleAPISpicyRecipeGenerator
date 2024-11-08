import requests
import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv('SPOONACULAR_API_KEY')

def test_api():
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "number": 1, 
        "addRecipeInformation": True
    }
    
    print(f"Testing API with key: {API_KEY[:5]}...")  
    response = requests.get(url, params=params)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("\nAPI Response:")
        print(data)
    else:
        print(f"Error Response: {response.text}")

if __name__ == "__main__":
    test_api()