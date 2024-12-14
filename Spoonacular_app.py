import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from flask import Flask, render_template, request, jsonify
from logging_config import setup_logger

# Setup logging
logger = setup_logger()

# Try to load from .env file, but don't fail if it doesn't exist
load_dotenv(override=True)

# Get API key from environment variable
API_KEY = os.getenv('SPOONACULAR_API_KEY')
if not API_KEY:
    raise ValueError("No API key found. Please set SPOONACULAR_API_KEY environment variable")

app = Flask(__name__)

def get_random_recipes(number=3, tags="", exclude_ingredients=None):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "number": number * 2,
        "sort": "random",
        "addRecipeInformation": True,
        "fillIngredients": True,
        "instructionsRequired": True,
        "tags": tags,
        "type": "main course",
        "excludeCuisine": "beverage",
    }
    
    if exclude_ingredients:
        params["excludeIngredients"] = ",".join(exclude_ingredients)
    
    logger.info("Fetching recipes with params: %s", {k: v for k, v in params.items() if k != 'apiKey'})
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        recipes = [r for r in data.get("results", []) 
                  if not any(dtype.lower() in ['drink', 'beverage', 'cocktail', 'alcohol'] 
                           for dtype in r.get('dishTypes', []))
                  and not (
                      ('soup' in r.get('dishTypes', []) or 'salad' in r.get('dishTypes', [])) 
                      and 'main course' not in r.get('dishTypes', [])
                  )]
        
        logger.info("Successfully fetched %d recipes", len(recipes))
        return recipes[:number]
        
    except requests.exceptions.RequestException as e:
        logger.error("API request failed: %s", str(e))
        return None
    except ValueError as e:
        logger.error("Failed to parse API response: %s", str(e))
        return None
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return None

def print_recipe(recipe: Dict):
    print("\n" + "="*50)
    print(f"Title: {recipe['title']}")
    print(f"Type: {', '.join(recipe.get('dishTypes', ['Not specified']))}")
    print(f"Ready in: {recipe['readyInMinutes']} minutes")
    print(f"Servings: {recipe['servings']}")
    print(f"Health Score: {recipe['healthScore']}/100")
    print(f"Spoonacular Score: {recipe.get('spoonacularScore', 'N/A')}/100")
    
    print("\nDietary Info:")
    print(f"- Vegetarian: {recipe['vegetarian']}")
    print(f"- Vegan: {recipe['vegan']}")
    print(f"- Gluten Free: {recipe['glutenFree']}")
    print(f"- Dairy Free: {recipe['dairyFree']}")
    
    if recipe.get('extendedIngredients'):
        print("\nIngredients:")
        for ingredient in recipe['extendedIngredients']:
            print(f"- {ingredient['original']}")
    
    print(f"\nCooking Instructions: {recipe['sourceUrl']}")
    print(f"Cuisine: {', '.join(recipe.get('cuisines', ['Not specified']))}")
    print("="*50 + "\n")

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if request.method == 'POST':
            logger.info("Processing POST request for recipe search")
            
            exclude_ingredients = ["pork", "red meat", "dairy", "wheat", "whey", "rye", "barley", "cheese", "milk", "cream"]
            search_tags = ["spicy"]
            
            recipes = get_random_recipes(
                number=5,
                tags=",".join(search_tags),
                exclude_ingredients=exclude_ingredients
            )
            
            if recipes:
                filtered_recipes = [r for r in recipes 
                                  if r.get('dishTypes') and 
                                  not any(t.lower() in ['drink', 'beverage', 'cocktail', 'alcohol'] 
                                        for t in r['dishTypes'])]
                
                logger.info("Found %d recipes after filtering", len(filtered_recipes))
                return render_template('index.html', recipes=filtered_recipes)
            
            logger.warning("No recipes found matching criteria")
            return render_template('index.html', error="No recipes found matching your criteria.")
        
        logger.info("Serving GET request for home page")
        return render_template('index.html')
        
    except Exception as e:
        logger.error("Error in home route: %s", str(e))
        return render_template('index.html', error="An unexpected error occurred. Please try again later.")

@app.errorhandler(404)
def not_found_error(error):
    logger.error('Page not found: %s', request.url)
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error('Server Error: %s', str(error))
    return render_template('index.html', error="An internal error occurred. Please try again later."), 500

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0', port=5000)