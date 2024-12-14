import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()
API_KEY = os.getenv('SPOONACULAR_API_KEY')

def get_random_recipes(number=3, tags="", exclude_ingredients=None):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": API_KEY,
        "number": number * 2,  # Request more to account for filtering
        "sort": "random",
        "addRecipeInformation": True,
        "fillIngredients": True,
        "instructionsRequired": True,
        "tags": tags,
        "type": "main course,soup,salad",  # no beverages or side dishes just main courses
        "excludeCuisine": "beverage",  # Explicitly exclude beverages, because sometimes they sneak in (martinis was a hilarious one)
    }
    
    if exclude_ingredients:
        params["excludeIngredients"] = ",".join(exclude_ingredients)
    
    print("\nFetching recipes...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        recipes = [r for r in data.get("results", []) 
                  if not any(dtype.lower() in ['drink', 'beverage', 'cocktail', 'alcohol'] 
                           for dtype in r.get('dishTypes', []))]
        return recipes[:number]  
    else:
        print(f"Error {response.status_code}: {response.text}")
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

def main():
    print("Welcome to the Spicy, Gluten/Dairy-Free Recipe Finder!")
    
    if not API_KEY:
        print("Error: No API key found. Please set SPOONACULAR_API_KEY in .env file")
        return
    
    exclude_ingredients = ["pork", "red meat", "dairy", "wheat", "whey", "rye", "barley", "cheese", "milk", "cream"]
    search_tags = ["spicy"]
    
    print(f"\nSearching for spicy recipes excluding: {', '.join(exclude_ingredients)}")
    print("Looking for main courses, soups, salads, and side dishes...")
    
    recipes = get_random_recipes(
        number=5,
        tags=",".join(search_tags),
        exclude_ingredients=exclude_ingredients
    )
    
    if recipes:
        # Additional filtering for food-only recipes b/c sometimes cocktail recipes sneak in
        filtered_recipes = [r for r in recipes 
                          if r.get('dishTypes') and 
                          not any(t.lower() in ['drink', 'beverage', 'cocktail', 'alcohol'] 
                                for t in r['dishTypes'])]
        
        if filtered_recipes:
            print(f"\nFound {len(filtered_recipes)} food recipes!")
            for recipe in filtered_recipes:
                print_recipe(recipe)
        else:
            print("\nNo suitable food recipes found after filtering.")
    else:
        print("\nNo recipes found matching your criteria.")
    
    print("\nThank you for using the Spicy, Gluten/Dairy-Free Recipe Finder!")

if __name__ == "__main__":
    main()