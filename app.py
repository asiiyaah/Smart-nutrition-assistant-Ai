
import streamlit as st
import torch
from torchvision.models import resnet50, ResNet50_Weights
from torchvision import transforms
from utils.nutrition import get_nutrition
from utils.meal_gen import generate_recipe
from utils.portion_vis import (
    classify_foods,
    nutrition_feedback
)


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



st.set_page_config(
    page_title="Smart Nutrition Assistant",
    layout="centered"
)

st.title("🥗 Smart Nutrition Assistant")

st.markdown("""
Welcome to the **Smart Nutrition Assistant**.

This app helps you:
- 🔍 Find calories and nutrition
- 🍳 Generate meals from ingredients
- 🖼️ Visualize proper food portion sizes using AI
""")

tab1, tab2, tab3 = st.tabs([
    "🥗 Smart Meal Analyzer",
    "🍳 Meal Generator",
    "🔍 Calories Finder"
])

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
                food_categories = classify_foods(foods)

            st.subheader("🍽️ Food Categories")
            for food, category in food_categories.items():
                st.write(f"• **{food.title()}** → {category.capitalize()}")

            with st.spinner("Generating nutrition feedback..."):
                feedback = nutrition_feedback(food_categories)

            st.subheader("🧠 Nutrition Feedback & Suggestions")
            st.markdown(feedback)

with tab2:
    st.header("🍳 AI Meal Generator")

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
                recipe = generate_recipe(ingredients, meal_type, diet)

            st.success("🍽️ Generated Recipe")
            st.markdown(recipe)
            st.caption("⚠️ Recipe is AI-generated using Google Gemini.")

with tab3:
    st.header("Calories & Nutrition Finder")

    uploaded_file = st.file_uploader(
        "Upload a food image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        # Show image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Preprocess
        input_tensor = preprocess(image).unsqueeze(0)

        # Predict
        with torch.no_grad():
            outputs = model(input_tensor)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)

        top_prob, top_idx = torch.topk(probs, 1)

        # Convert class index → label
        predicted_label = weights.meta["categories"][top_idx.item()]
        food_name = predicted_label.lower()

        
        # Nutrition lookup
        nutrition = get_nutrition(food_name)

        if nutrition:
            st.success(f"Predicted food: **{nutrition['Food']}**")
        else:
            st.success(f"Predicted food: **{food_name}**")


        if nutrition:
            st.subheader("Nutrition Information")
            st.write(f"🔥 Calories: {nutrition['Calories']} kcal")
            st.write(f"💪 Protein: {nutrition['Protein']} g")
            st.write(f"🍞 Carbs: {nutrition['Carbs']} g")
            st.write(f"🧈 Fat: {nutrition['Fat']} g")
            st.write(f"🍥 Sugars: {nutrition['Sugars']} g")
            st.write(f"🌾 Fiber: {nutrition['Fiber']} g" )
        else:
            st.warning("Nutrition data not found for this food.")





