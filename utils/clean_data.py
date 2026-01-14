import pandas as pd
import re

data = pd.read_csv(
    '../data/food_nutrition_dataset.csv',
    on_bad_lines='skip'
)

def clean_food_name(name):
    name = name.lower()
    name = re.sub(r'\(.*?\)', '', name)  # remove brackets
    name = re.sub(r'\d+', '', name)      # remove numbers
    name = name.strip()
    return name


# Remove missing & duplicates
data = data.dropna()
data = data.drop_duplicates()

data = data.rename(columns={
    'Food_Item': 'Food',
    'Calories (kcal)': 'Calories',
    'Protein (g)': 'Protein',
    'Carbohydrates (g)': 'Carbs',
    'Fat (g)': 'Fat',
    'Fiber (g)': 'Fiber',
    'Sugars (g)': 'Sugars',
    'Cholesterol (mg)': 'Cholesterol'
})
data['Food'] = data['Food'].apply(clean_food_name)

# Keep only required columns
data = data[['Food', 'Calories', 'Protein', 'Carbs', 'Fat', 'Fiber', 'Sugars', 'Cholesterol']]

# Clean text
data['Food'] = data['Food'].str.lower()

# Convert numeric columns
cols = ['Calories', 'Protein', 'Carbs', 'Fat', 'Fiber', 'Sugars', 'Cholesterol']
for col in cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Remove rows with conversion errors
data = data.dropna()

# Save cleaned data
data.to_csv('../data/cleaned_food_data.csv', index=False)

print("Cleaning completed successfully!")
print(data.head(10))
print("Final shape:", data.shape)
