The Spicy, Gluten/Dairy-Free Recipe Finder
Powered by Spoonacular

A Python application that fetches and filters recipes using the Spoonacular API specifically geared to retrieve spicier meals - no gluten or dairy, pork, or red meat.

1. **Set Up: Get a Spoonacular API Key**
   - Sign up at [spoonacular.com](https://spoonacular.com)
   - Go to [Spoonacular Food API](https://spoonacular.com/food-api)
   - Click "Start Now"
   - Navigate to "Profile & API Key"
   - Generate and immediately copy your own API key, save it

2. **Set Up the Project**

   git clone https://github.com/leighanne77/SimpleAPISpicyRecipeGenerator.git
   cd SimpleAPISpicyRecipeGenerator

   Mac: you will need to run "conda deactivate" if you are using anaconda
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   pip install -r requirements.txt

   # create and then add Spoonacular API key to an .env file in the project root 
   SPOONACULAR_API_KEY=your_api_key_here

   # Test the Setup
   python test.py
   python test_api.py

   # Run the Application
   python spoonacular_app.py
   
## Project Structure
- `Spoonacular_app.py`: Main application file
- `test.py`: Test utilities
- `test_api.py`: API testing and validation
- `config.yaml`: Configuration settings
- `requirements.txt`: Project dependencies
