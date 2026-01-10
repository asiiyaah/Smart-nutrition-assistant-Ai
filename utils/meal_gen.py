# utils/meal_gen.py

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_recipe(ingredients, meal_type, diet):
    prompt = f"""
You are a helpful cooking assistant.

Create ONE simple and practical recipe.

Main ingredients provided by the user (these MUST be used):
{ingredients}

You MAY additionally use small basic cooking items such as:
salt, oil, water, butter, basic spices, herbs.

DO NOT introduce any major new ingredients beyond the ones provided.

Meal type: {meal_type}
Diet preference: {diet}

Respond STRICTLY in this format:

Dish Name:
Ingredients Used:
- list all ingredients (including basic ones)

Recipe Steps:
1. step one
2. step two
3. step three
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
