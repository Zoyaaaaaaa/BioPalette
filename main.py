
import streamlit as st
from PIL import Image
import google.generativeai as genai
import time
from typing import List, Dict


def initialize_api():
    try:
        api_key = st.secrets["GEMINI_API_KEY"] 
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error("Error initializing API. Please check your API key.")
        return False


PRESET_MOODS = [
    "🎒 Adventurous", "🎨 Artistic", "☮️ Peaceful", "⚡ Energetic", 
    "💼 Professional", "💖 Romantic", "🕵️‍♀️ Mysterious", "🎲 Playful", 
    "🌅 Inspirational", "🌿 Nature-loving", "💻 Tech-savvy", "🍕 Foodie", 
    "👗 Fashion-forward", "🧘 Spiritual", "🏃 Athletic"
]

MOOD_MODIFIERS = {
    "Tone Modifiers": ["😂 Humorous", "🧐 Serious", "🙃 Sarcastic", "📝 Poetic", "🔍 Minimalist", "🎭 Elaborate"],
    "Style Elements": ["💡 Emoji-rich", "📜 Quote-based", "🏷️ Hashtag-friendly", "🔠 Wordplay", "🕵️ Mysterious", "📚 Traditional"],
    "Personality Traits": ["😎 Confident", "🙏 Humble", "🤪 Quirky", "🎩 Sophisticated", "🌍 Down-to-earth", "🌌 Dreamy"]
}


st.set_page_config(
    page_title="✨ Instagram Bio Generator ✨",
    layout="centered",
    page_icon="🌙",
    initial_sidebar_state="collapsed"
)


st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .stButton > button {
            background-color: #4FD1C5;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #38B2AC;
        }
        .bio-box {
            padding: 1rem;
            background-color: #1f1f1f;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        .mood-section {
            background-color: #1f1f1f;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        .custom-mood {
            margin-top: 1rem;
            padding: 0.5rem;
            border-top: 1px solid #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)

def get_gemini_response(image_parts: List[Dict], prompt: str, retries: int = 3) -> str:
    """Generate response from Gemini API with retry mechanism."""
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([image_parts[0], prompt])
            return response.text
        except Exception as e:
            if attempt == retries - 1:
                raise Exception(f"Failed after {retries} attempts: {str(e)}")
            time.sleep(1)

def input_image_setup(uploaded_file) -> List[Dict]:
    """Process uploaded image and return in format required by Gemini API."""
    if not uploaded_file:
        raise ValueError("Please upload an image.")
    try:
        image = Image.open(uploaded_file)
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')
        bytes_data = uploaded_file.getvalue()
        if len(bytes_data) > 4 * 1024 * 1024:
            raise ValueError("Image size too large. Upload an image smaller than 4MB.")
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

def generate_bio_prompt(base_mood: str, modifiers: List[str], custom_mood: str, num_bios: int) -> str:
    """Generate prompt for bio creation."""
    mood_description = base_mood
    if modifiers:
        mood_description += f" with elements of {', '.join(modifiers)}"
    if custom_mood:
        mood_description += f" and {custom_mood}"

    return f"""
    As an Instagram bio expert, create {num_bios} unique bios matching this mood: {mood_description}.

    Guidelines:
    - Each bio under 150 characters.
    - Use relevant emojis.
    - Make them catchy and memorable.
    - Match the mood and image.
    - Incorporate the specified modifiers.
    - 9Give only bio on each new line nothing else.
    """

def main():
    st.markdown("<h1 style='text-align: center;'>✨ Instagram Bio Generator ✨</h1>", unsafe_allow_html=True)
    st.markdown("### Transform your photos into engaging Instagram bios!")

    uploaded_file = st.file_uploader("Upload your image (JPG, JPEG, or PNG)", type=["jpg", "jpeg", "png"], help="Max size: 4MB")

    st.markdown("### 🎨 Choose Your Vibe")

    col1, col2 = st.columns([2, 1])
    with col1:
        base_mood = st.selectbox("Select Base Mood", options=PRESET_MOODS)
        custom_mood = st.text_input("Add Custom Mood (optional)", placeholder="e.g., Wanderlust, Coffee lover")

        with st.expander("✨ Add Mood Modifiers", expanded=True):
            selected_modifiers = []
            for category, modifiers in MOOD_MODIFIERS.items():
                st.write(f"**{category}**")
                cols = st.columns(3)
                for i, modifier in enumerate(modifiers):
                    with cols[i % 3]:
                        if st.checkbox(modifier, key=f"mod_{modifier}"):
                            selected_modifiers.append(modifier)

    with col2:
        num_bios = st.slider("Number of bios", 1, 5, 3)
        st.markdown("**Selected Modifiers:**")
        for modifier in selected_modifiers:
            st.markdown(f"- {modifier}")

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview", use_column_width=True)
        except Exception as e:
            st.error(f"Error displaying image: {str(e)}")
            return

    if st.button("✨ Generate Bios", disabled=not (uploaded_file and base_mood)):
        with st.spinner("Crafting your perfect bios..."):
            try:
                image_data = input_image_setup(uploaded_file)
                prompt = generate_bio_prompt(base_mood, selected_modifiers, custom_mood, num_bios)
                response = get_gemini_response(image_data, prompt)

                st.markdown("### 📝 Your Generated Bios:")
                bios = [bio.strip() for bio in response.split('\n') if bio.strip()]
                for i, bio in enumerate(bios[:num_bios], 1):
                    st.markdown(f"<div class='bio-box'>{bio}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating bios: {str(e)}")
                st.info("Try again with a different image or refresh the page.")

    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(45deg, #4FD1C5, #F5D0A9); border-radius: 8px;">
            <p>Made by Zoya</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
