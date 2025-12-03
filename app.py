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
    
    # Handle case where no recipe found
    if not recipe:
        return render_template("index.html",
                               searched_food=food_name,
                               videos=videos,
                               error="Sorry, I couldn't find a recipe for that food. Try a different name!")
    
    return render_template("index.html",
                           searched_food=food_name,
                           recipe=recipe,
                           videos=videos)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)