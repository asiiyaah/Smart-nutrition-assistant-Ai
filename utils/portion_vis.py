import os
import json
import re
import google.generativeai as genai


# Gemini configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# 1️⃣ Classify foods into categories
def classify_foods(food_list):
    """
    Classifies foods into nutrition categories using Gemini.
    Returns a dict: { food_name: category }
    """

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a nutrition expert.

    Classify each food into ONE of these categories only:
    - vegetables
    - protein
    - carbohydrates
    - fats
    - mixed

    Foods:
    {", ".join(food_list)}

    Return ONLY valid JSON.
    """

    response = model.generate_content(prompt)
    text = response.text

    # Clean markdown if Gemini adds it
    text = re.sub(r"```json|```", "", text).strip()

    return json.loads(text)


# 2️⃣ Nutrition feedback & suggestions
def nutrition_feedback(food_categories):
    """
    Analyzes nutritional balance and suggests improvements.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a nutrition expert.

    Given the following food categories:
    {food_categories}

    Perform the following:
    1. Identify nutritional imbalances (excess or missing food groups)
    2. Mention what is good about the meal (if any)
    3. Suggest practical improvements for a balanced, healthy meal
    4. Keep suggestions simple and Indian-diet friendly

    Respond clearly using bullet points.
    """

    response = model.generate_content(prompt)
    return response.text
