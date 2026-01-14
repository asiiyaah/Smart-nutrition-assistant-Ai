import streamlit as st
import torch
from PIL import Image
from torchvision.models import resnet50, ResNet50_Weights
from torchvision import transforms

from utils.nutrition import get_nutrition
from utils.meal_gen import generate_recipe
from utils.portion_vis import classify_foods, nutrition_feedback


# ---------------------------------
# Load image model (cached)
# ---------------------------------
@st.cache_resource
def load_model():
    weights = ResNet50_Weights.IMAGENET1K_V2
    model = resnet50(weights=weights)
    model.eval()
    return model, weights

model, weights = load_model()

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# ---------------------------------
# Streamlit config
# ---------------------------------
st.set_page_config(
    page_title="Smart Nutrition Assistant",
    layout="centered"
)

st.title("🥗 Smart Nutrition Assistant")

st.markdown("""
Welcome to the **Smart Nutrition Assistant**.

This app helps you:
- 🔍 Find calories and nutrition from food images
- 🍳 Generate meals using available ingredients
- 🥗 Analyze meal balance and get nutrition advice
""")


# ---------------------------------
# Session state initialization
# ---------------------------------
if "meal_categories" not in st.session_state:
    st.session_state.meal_categories = None
if "meal_feedback" not in st.session_state:
    st.session_state.meal_feedback = None

if "recipe" not in st.session_state:
    st.session_state.recipe = None

if "nutrition_result" not in st.session_state:
    st.session_state.nutrition_result = None


# ---------------------------------
# Tabs
# ---------------------------------
tab1, tab2, tab3 = st.tabs([
    "🥗 Smart Meal Analyzer",
    "🍳 Meal Generator",
    "🔍 Calories Finder"
])


# =====================================================
# TAB 1: Smart Meal Analyzer
# =====================================================
with tab1:
    st.header("🥗 Smart Meal Analyzer")

    st.markdown(
        """
        This feature helps you understand **how balanced your meal is**.

        👉 Enter the foods you plan to eat, and the system will:
        - Classify each food into nutrition groups  
        - Identify missing or excess nutrients  
        - Suggest simple improvements for a healthier meal  

        This analysis is AI-driven and focuses on **practical, everyday meals**.
        """
    )

    food_input = st.text_input(
        "Enter foods you plan to eat (comma separated)",
        placeholder="rice, brinjal fry, mashed potato, almonds"
    )

    if st.button("Analyze Meal"):
        foods = [f.strip() for f in food_input.split(",") if f.strip()]

        if not foods:
            st.warning("Please enter at least one food.")
        else:
            with st.spinner("Analyzing meal..."):
                st.session_state.meal_categories = classify_foods(foods)
                st.session_state.meal_feedback = nutrition_feedback(
                    st.session_state.meal_categories
                )

    if st.session_state.meal_categories:
        st.subheader("🍽️ Food Categories")
        for food, category in st.session_state.meal_categories.items():
            st.write(f"• **{food.title()}** → {category.capitalize()}")

    if st.session_state.meal_feedback:
        st.subheader("🧠 Nutrition Feedback & Suggestions")
        st.markdown(st.session_state.meal_feedback)


# =====================================================
# TAB 2: Meal Generator
# =====================================================
with tab2:
    st.header("🍳 AI Meal Generator")

    st.markdown(
        """
        This feature helps you create a meal using the ingredients you already have.

        👉 Enter the available ingredients, choose the type of meal and your diet preference, and the system will:
        - Generate a complete recipe using AI  
        - Suggest simple preparation steps  
        - Adapt the recipe to your meal type and diet choice  

        This is useful when you’re unsure what to cook or want quick meal ideas.
        """
    )

    ingredients = st.text_area(
        "Enter available ingredients (comma separated)",
        placeholder="e.g. rice, tomato, onion, egg"
    )

    meal_type = st.selectbox(
        "Type of meal",
        ["Breakfast", "Lunch", "Dinner", "Snack"]
    )

    diet = st.selectbox(
        "Diet preference",
        ["Any", "Vegetarian", "Non-Vegetarian"]
    )

    if st.button("Generate Recipe"):
        if not ingredients.strip():
            st.warning("Please enter ingredients.")
        else:
            with st.spinner("Generating recipe using AI..."):
                st.session_state.recipe = generate_recipe(
                    ingredients, meal_type, diet
                )

    if st.session_state.recipe:
        st.success("🍽️ Generated Recipe")
        st.markdown(st.session_state.recipe)
        st.caption("⚠️ Recipe is AI-generated using Google Gemini.")


# =====================================================
# TAB 3: Calories Finder
# =====================================================
with tab3:
    st.header("🔍 Calories & Nutrition Finder")

    st.markdown(
        """
        This feature estimates calories and nutritional values from a food image.

        ⚠️ **Note:** This tool works best for **single food items only**.  
        Please upload an image containing one clearly visible food item.

        👉 The system will:
        - Identify the food item using an AI image model  
        - Display approximate calorie and nutrition information  

        For meals with multiple foods, use the **Smart Meal Analyzer** instead.
        """
    )
    st.info(
    "ℹ️ This feature uses a pre-trained image model and currently performs best on "
    "clear, common food items (e.g., orange, ice cream, apple). "
    "More training and fine-tuning are required for accurate recognition of complex or mixed dishes."
)

    uploaded_file = st.file_uploader(
        "Upload a food image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        input_tensor = preprocess(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(input_tensor)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)

        _, top_idx = torch.topk(probs, 1)
        predicted_label = weights.meta["categories"][top_idx.item()]
        food_name = predicted_label.lower()

        nutrition = get_nutrition(food_name)
        st.session_state.nutrition_result = (food_name, nutrition)

    if st.session_state.nutrition_result:
        food_name, nutrition = st.session_state.nutrition_result

        if nutrition:
            st.success(f"Predicted food: **{nutrition['Food']}**")
            st.subheader("Nutrition Information")
            st.write(f"🔥 Calories: {nutrition['Calories']} kcal")
            st.write(f"💪 Protein: {nutrition['Protein']} g")
            st.write(f"🍞 Carbs: {nutrition['Carbs']} g")
            st.write(f"🧈 Fat: {nutrition['Fat']} g")
            st.write(f"🍥 Sugars: {nutrition['Sugars']} g")
            st.write(f"🌾 Fiber: {nutrition['Fiber']} g")
        else:
            st.success(f"Predicted food: **{food_name}**")
            st.warning("Nutrition data not found for this food.")
