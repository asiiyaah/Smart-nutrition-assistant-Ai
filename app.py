import streamlit as st

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
    st.write("Coming soon...")

with tab2:
    st.header("Meal Generator from Ingredients")
    st.write("Coming soon...")

with tab3:
    st.header("Food Plating & Portion Size Visualizer")
    st.write("Coming soon...")
