# 🥗 Smart Nutrition Assistant

The **Smart Nutrition Assistant** is a Streamlit-based web application that helps users make healthier food choices using AI.  
It combines image-based food recognition, AI-powered meal analysis, and recipe generation into a single application.

---

## ✨ Features

### 🥗 Smart Meal Analyzer
- Users enter foods they plan to eat
- AI classifies foods into nutrition categories
- Identifies missing or excess nutrients
- Provides practical suggestions to improve meal balance

---

### 🍳 AI Meal Generator
- Generates recipes based on available ingredients
- Supports different meal types (Breakfast, Lunch, Dinner, Snack)
- Supports vegetarian and non-vegetarian preferences
- Useful for quick and easy meal ideas

---

### 🔍 Calories & Nutrition Finder
- Users upload an image of a food item
- AI predicts the food and displays calorie & nutrition information
- Works best for **single, clearly visible food items**

⚠️ **Note:**  
This feature currently performs best on common foods such as fruits or desserts (e.g., orange, ice cream).  
More training and fine-tuning are required for accurate recognition of complex or mixed dishes.

---

## 🧠 Technologies Used
- Python
- Streamlit
- PyTorch & Torchvision
- ResNet50 (ImageNet pre-trained)
- Google Gemini API
- Pillow (PIL)

---

## 🚀 How to Run the Project Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/asiiyaah/Smart-nutrition-assistant-Ai
cd smart-nutrition-assistant

### 2️⃣ Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt

### 4️⃣ Set Environment Variables

Set your **Google Gemini API key**.

**Linux / macOS**
```bash
export GOOGLE_API_KEY="your_api_key_here"


5️⃣ Run the application
```bash
streamlit run app.py


The app will open in your browser.

# 📁 Project Structure
├── app.py
├── utils/
│   ├── nutrition.py
│   ├── meal_gen.py
│   └── portion_vis.py
├── requirements.txt
└── README.md

# ⚠️ Limitations

•Image-based calorie estimation works best for single food items

•Complex or mixed dishes may not be accurately recognized

•Nutrition values are approximate

•Image model uses a pre-trained dataset and is not fine-tuned

#🔮 Future Improvements

•Fine-tune the image model for complex dishes

•Add daily meal tracking

•Personalized diet recommendations

•Portion size estimation

# 👤 Author
Developed by **Asiya Muhammed Sali Thachavallath**,  
