
import streamlit as st
import torch
from torchvision.models import resnet50, ResNet50_Weights
from torchvision import transforms
from PIL import Image

from utils.nutrition import get_nutrition

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
    "🔍 Calories Finder",
    "🍳 Meal Generator",
    "🖼️ Portion Visualizer"
])

with tab1:
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

with tab2:
    st.header("Meal Generator from Ingredients")
    st.write("Coming soon...")

with tab3:
    st.header("Food Plating & Portion Size Visualizer")
    st.write("Coming soon...")
