# utils/nutrition.py
import pandas as pd
import re

# Load cleaned dataset ONCE
df = pd.read_csv("data/cleaned_food_data.csv")


def normalize_name(name: str) -> str:
    """
    Normalize food name for matching:
    - lowercase
    - remove anything inside brackets
    - strip extra spaces
    """
    name = name.lower()
    name = re.sub(r"\(.*?\)", "", name)  # remove ( ... )
    return name.strip()


def get_nutrition(food_name):
    food_name_norm = normalize_name(food_name)

    # Normalize dataset food names 
    df["_normalized_food"] = df["Food"].astype(str).apply(normalize_name)

    row = df[df["_normalized_food"] == food_name_norm]

    if row.empty:
        return None

    return {
        #  keeps the bracket info for display
        "Food": row.iloc[0]["Food"],

        "Calories": row.iloc[0]["Calories"],
        "Protein": row.iloc[0]["Protein"],
        "Carbs": row.iloc[0]["Carbs"],
        "Fat": row.iloc[0]["Fat"],
        "Sugars": row.iloc[0]["Sugars"],
        "Fiber": row.iloc[0]["Fiber"],
    }
