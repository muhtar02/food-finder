# app.py - Main Flask Application for Food Finder

from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# API Configuration
MEALDB_API = "https://www.themealdb.com/api/json/v1/1"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API = "https://www.googleapis.com/youtube/v3"
NUTRITIONIX_API = "https://trackapi.nutritionix.com/v2/natural/nutrients"

# Homepage route
@app.route("/")
def home():
    """Show the homepage with search box"""
    return render_template("index.html")

def get_recipe(food_name):
    """Fetch recipe from TheMealDB API"""
    try:
        response = requests.get(f"{MEALDB_API}/search.php?s={food_name}")
        data = response.json()
        
        if data["meals"]:
            meal = data["meals"][0]
            
            # Extract ingredients and measurements
            ingredients = []
            for i in range(1, 21):
                ingredient = meal.get(f"strIngredient{i}", "")
                measure = meal.get(f"strMeasure{i}", "")
                if ingredient and ingredient.strip():
                    ingredient_name = ingredient.strip()
                    ingredients.append({
                        "name": ingredient_name,
                        "measure": measure.strip() if measure else "",
                        "amazon_link": f"https://www.amazon.com/s?k={quote_plus(ingredient_name)}",
                        "google_link": f"https://www.google.com/search?tbm=shop&q={quote_plus(ingredient_name)}"
                    })
            
            return {
                "name": meal.get("strMeal", "Unknown"),
                "image": meal.get("strMealThumb", ""),
                "category": meal.get("strCategory", ""),
                "cuisine": meal.get("strArea", ""),
                "instructions": meal.get("strInstructions", ""),
                "ingredients": ingredients
            }
    except Exception as e:
        print(f"Recipe API Error: {e}")
    
    return None

def get_youtube_videos(food_name):
    """Fetch tutorial videos from YouTube API"""
    if not YOUTUBE_API_KEY:
        print("YouTube API key not found!")
        return []
    
    try:
        search_query = f"{food_name} recipe cooking tutorial"
        params = {
            "part": "snippet",
            "q": search_query,
            "key": YOUTUBE_API_KEY,
            "maxResults": 6,
            "type": "video",
            "relevanceLanguage": "en"
        }
        
        response = requests.get(f"{YOUTUBE_API}/search", params=params)
        data = response.json()
        
        if "error" in data:
            print(f"YouTube API Error: {data['error']['message']}")
            return []
        
        videos = []
        for item in data.get("items", []):
            video = {
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "video_id": item["id"]["videoId"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)
        
        return videos
    
    except Exception as e:
        print(f"YouTube API Error: {e}")
        return []

def get_nutrition_info(food_name):
    """Estimate nutrition info based on recipe category and common values"""
    # Since Nutritionix requires paid API, we'll use estimated values
    # based on common food categories
    nutrition_estimates = {
        "Beef": {"calories": 450, "protein": 35, "carbs": 20, "fat": 25, "fiber": 3},
        "Chicken": {"calories": 350, "protein": 40, "carbs": 15, "fat": 12, "fiber": 2},
        "Seafood": {"calories": 300, "protein": 35, "carbs": 10, "fat": 10, "fiber": 1},
        "Vegetarian": {"calories": 280, "protein": 15, "carbs": 40, "fat": 8, "fiber": 8},
        "Vegan": {"calories": 250, "protein": 12, "carbs": 45, "fat": 6, "fiber": 10},
        "Pasta": {"calories": 550, "protein": 18, "carbs": 70, "fat": 18, "fiber": 4},
        "Dessert": {"calories": 450, "protein": 6, "carbs": 65, "fat": 20, "fiber": 2},
        "Breakfast": {"calories": 400, "protein": 20, "carbs": 45, "fat": 15, "fiber": 3},
        "Side": {"calories": 200, "protein": 5, "carbs": 30, "fat": 8, "fiber": 4},
        "Starter": {"calories": 250, "protein": 10, "carbs": 25, "fat": 12, "fiber": 3},
        "Lamb": {"calories": 480, "protein": 32, "carbs": 18, "fat": 30, "fiber": 2},
        "Pork": {"calories": 420, "protein": 30, "carbs": 20, "fat": 25, "fiber": 2},
        "Goat": {"calories": 400, "protein": 35, "carbs": 15, "fat": 20, "fiber": 2},
        "Miscellaneous": {"calories": 380, "protein": 20, "carbs": 35, "fat": 15, "fiber": 4},
    }
    
    return nutrition_estimates.get(food_name, {
        "calories": 350, "protein": 20, "carbs": 35, "fat": 15, "fiber": 4
    })

# Search route
@app.route("/search")
def search():
    """Handle search requests"""
    food_name = request.args.get("food", "").strip()
    
    if not food_name:
        return render_template("index.html")
    
    # Get recipe
    recipe = get_recipe(food_name)
    
    # Get YouTube videos
    videos = get_youtube_videos(food_name)
    
    # Get nutrition info based on category
    nutrition = None
    if recipe:
        nutrition = get_nutrition_info(recipe.get("category", ""))
    
    # Handle case where no recipe found
    if not recipe:
        return render_template("index.html",
                               searched_food=food_name,
                               videos=videos,
                               error="Sorry, I couldn't find a recipe for that food. Try a different name!")
    
    return render_template("index.html",
                           searched_food=food_name,
                           recipe=recipe,
                           videos=videos,
                           nutrition=nutrition)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)