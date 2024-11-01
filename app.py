
# import streamlit as st
# from PIL import Image
# import google.generativeai as genai
# import time
# from typing import List, Dict


# def initialize_api():
#     try:
#         api_key = st.secrets["GEMINI_API_KEY"] 
#         genai.configure(api_key=api_key)
#         return True
#     except Exception as e:
#         st.error("Error initializing API. Please check your API key.")
#         return False


# PRESET_MOODS = [
#     "🎒 Adventurous", "🎨 Artistic", "☮️ Peaceful", "⚡ Energetic", 
#     "💼 Professional", "💖 Romantic", "🕵️‍♀️ Mysterious", "🎲 Playful", 
#     "🌅 Inspirational", "🌿 Nature-loving", "💻 Tech-savvy", "🍕 Foodie", 
#     "👗 Fashion-forward", "🧘 Spiritual", "🏃 Athletic"
# ]

# MOOD_MODIFIERS = {
#     "Tone Modifiers": ["😂 Humorous", "🧐 Serious", "🙃 Sarcastic", "📝 Poetic", "🔍 Minimalist", "🎭 Elaborate"],
#     "Style Elements": ["💡 Emoji-rich", "📜 Quote-based", "🏷️ Hashtag-friendly", "🔠 Wordplay", "🕵️ Mysterious", "📚 Traditional"],
#     "Personality Traits": ["😎 Confident", "🙏 Humble", "🤪 Quirky", "🎩 Sophisticated", "🌍 Down-to-earth", "🌌 Dreamy"]
# }


# st.set_page_config(
#     page_title="✨ Instagram Bio Generator ✨",
#     layout="centered",
#     page_icon="🌙",
#     initial_sidebar_state="collapsed"
# )


# st.markdown("""
#     <style>
#         body {
#             background-color: #121212;
#             color: #ffffff;
#         }
#         .stButton > button {
#             background-color: #4FD1C5;
#             color: white;
#             border-radius: 8px;
#             padding: 0.5rem 1rem;
#             width: 100%;
#         }
#         .stButton > button:hover {
#             background-color: #38B2AC;
#         }
#         .bio-box {
#             padding: 1rem;
#             background-color: #1f1f1f;
#             border-radius: 8px;
#             margin: 0.5rem 0;
#         }
#         .mood-section {
#             background-color: #1f1f1f;
#             padding: 1rem;
#             border-radius: 8px;
#             margin: 0.5rem 0;
#         }
#         .custom-mood {
#             margin-top: 1rem;
#             padding: 0.5rem;
#             border-top: 1px solid #e2e8f0;
#         }
#     </style>
# """, unsafe_allow_html=True)

# def get_gemini_response(image_parts: List[Dict], prompt: str, retries: int = 3) -> str:
#     """Generate response from Gemini API with retry mechanism."""
#     for attempt in range(retries):
#         try:
#             model = genai.GenerativeModel('gemini-1.5-flash')
#             response = model.generate_content([image_parts[0], prompt])
#             return response.text
#         except Exception as e:
#             if attempt == retries - 1:
#                 raise Exception(f"Failed after {retries} attempts: {str(e)}")
#             time.sleep(1)

# def input_image_setup(uploaded_file) -> List[Dict]:
#     """Process uploaded image and return in format required by Gemini API."""
#     if not uploaded_file:
#         raise ValueError("Please upload an image.")
#     try:
#         image = Image.open(uploaded_file)
#         if image.mode not in ('RGB', 'L'):
#             image = image.convert('RGB')
#         bytes_data = uploaded_file.getvalue()
#         if len(bytes_data) > 4 * 1024 * 1024:
#             raise ValueError("Image size too large. Upload an image smaller than 4MB.")
#         return [{"mime_type": uploaded_file.type, "data": bytes_data}]
#     except Exception as e:
#         raise ValueError(f"Error processing image: {str(e)}")

# def generate_bio_prompt(base_mood: str, modifiers: List[str], custom_mood: str, num_bios: int) -> str:
#     """Generate prompt for bio creation."""
#     mood_description = base_mood
#     if modifiers:
#         mood_description += f" with elements of {', '.join(modifiers)}"
#     if custom_mood:
#         mood_description += f" and {custom_mood}"

#     return f"""
#     As an Instagram bio expert, create {num_bios} unique bios matching this mood: {mood_description}.

#     Guidelines:
#     - Each bio under 150 characters.
#     - Use relevant emojis.
#     - Make them catchy and memorable.
#     - Match the mood and image.
#     - Incorporate the specified modifiers.
#     - 9Give only bio on each new line nothing else.
#     """

# def main():
#     st.markdown("<h1 style='text-align: center;'>✨ Instagram Bio Generator ✨</h1>", unsafe_allow_html=True)
#     st.markdown("### Transform your photos into engaging Instagram bios!")

#     uploaded_file = st.file_uploader("Upload your image (JPG, JPEG, or PNG)", type=["jpg", "jpeg", "png"], help="Max size: 4MB")

#     st.markdown("### 🎨 Choose Your Vibe")

#     col1, col2 = st.columns([2, 1])
#     with col1:
#         base_mood = st.selectbox("Select Base Mood", options=PRESET_MOODS)
#         custom_mood = st.text_input("Add Custom Mood (optional)", placeholder="e.g., Wanderlust, Coffee lover")

#         with st.expander("✨ Add Mood Modifiers", expanded=True):
#             selected_modifiers = []
#             for category, modifiers in MOOD_MODIFIERS.items():
#                 st.write(f"**{category}**")
#                 cols = st.columns(3)
#                 for i, modifier in enumerate(modifiers):
#                     with cols[i % 3]:
#                         if st.checkbox(modifier, key=f"mod_{modifier}"):
#                             selected_modifiers.append(modifier)

#     with col2:
#         num_bios = st.slider("Number of bios", 1, 5, 3)
#         st.markdown("**Selected Modifiers:**")
#         for modifier in selected_modifiers:
#             st.markdown(f"- {modifier}")

#     if uploaded_file:
#         try:
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Preview", use_column_width=True)
#         except Exception as e:
#             st.error(f"Error displaying image: {str(e)}")
#             return

#     if st.button("✨ Generate Bios", disabled=not (uploaded_file and base_mood)):
#         with st.spinner("Crafting your perfect bios..."):
#             try:
#                 image_data = input_image_setup(uploaded_file)
#                 prompt = generate_bio_prompt(base_mood, selected_modifiers, custom_mood, num_bios)
#                 response = get_gemini_response(image_data, prompt)

#                 st.markdown("### 📝 Your Generated Bios:")
#                 bios = [bio.strip() for bio in response.split('\n') if bio.strip()]
#                 for i, bio in enumerate(bios[:num_bios], 1):
#                     st.markdown(f"<div class='bio-box'>{bio}</div>", unsafe_allow_html=True)
#             except Exception as e:
#                 st.error(f"Error generating bios: {str(e)}")
#                 st.info("Try again with a different image or refresh the page.")

#     st.markdown("""
#         <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: linear-gradient(45deg, #4FD1C5, #F5D0A9); border-radius: 8px;">
#             <p>Made by Zoya</p>
#         </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()
# # import os
# # import streamlit as st
# # from PIL import Image
# # import google.generativeai as genai
# # import time
# # from typing import List, Dict
# # from supabase import create_client, Client

# # # Initialize API
# # def initialize_api() -> bool:
# #     try:
# #         api_key = st.secrets["GEMINI_API_KEY"]
# #         genai.configure(api_key=api_key)
# #         return True
# #     except Exception as e:
# #         st.error("Error initializing API. Please check your API key.")
# #         return False

# # # Initialize Supabase client
# # def initialize_supabase() -> Client:
# #     url = st.secrets["SUPABASE_URL"]
# #     key = st.secrets["SUPABASE_KEY"]
# #     return create_client(url, key)

# # PRESET_MOODS = [
# #     "🎒 Adventurous", "🎨 Artistic", "☮️ Peaceful", "⚡ Energetic",
# #     "💼 Professional", "💖 Romantic", "🕵️‍♀️ Mysterious", "🎲 Playful",
# #     "🌅 Inspirational", "🌿 Nature-loving", "💻 Tech-savvy", "🍕 Foodie",
# #     "👗 Fashion-forward", "🧘 Spiritual", "🏃 Athletic"
# # ]

# # MOOD_MODIFIERS = {
# #     "Tone Modifiers": ["😂 Humorous", "🧐 Serious", "🙃 Sarcastic", "📝 Poetic", "🔍 Minimalist", "🎭 Elaborate"],
# #     "Style Elements": ["💡 Emoji-rich", "📜 Quote-based", "🏷️ Hashtag-friendly", "🔠 Wordplay", "🕵️ Mysterious", "📚 Traditional"],
# #     "Personality Traits": ["😎 Confident", "🙏 Humble", "🤪 Quirky", "🎩 Sophisticated", "🌍 Down-to-earth", "🌌 Dreamy"]
# # }

# # # Streamlit configuration
# # st.set_page_config(
# #     page_title="✨ Instagram Bio Generator ✨",
# #     layout="centered",
# #     page_icon="🌙",
# #     initial_sidebar_state="collapsed"
# # )

# # st.markdown("""
# #     <style>
# #         body {
# #             background-color: #121212;
# #             color: #ffffff;
# #         }
# #         .stButton > button {
# #             background-color: #4FD1C5;
# #             color: white;
# #             border-radius: 8px;
# #             padding: 0.5rem 1rem;
# #             width: 100%;
# #         }
# #         .stButton > button:hover {
# #             background-color: #38B2AC;
# #         }
# #         .bio-box {
# #             padding: 1rem;
# #             background-color: #1f1f1f;
# #             border-radius: 8px;
# #             margin: 0.5rem 0;
# #         }
# #         .mood-section {
# #             background-color: #1f1f1f;
# #             padding: 1rem;
# #             border-radius: 8px;
# #             margin: 0.5rem 0;
# #         }
# #     </style>
# # """, unsafe_allow_html=True)

# # def get_gemini_response(image_parts: List[Dict], prompt: str, retries: int = 3) -> str:
# #     """Generate response from Gemini API with retry mechanism."""
# #     for attempt in range(retries):
# #         try:
# #             model = genai.GenerativeModel('gemini-1.5-flash')
# #             response = model.generate_content([image_parts[0], prompt])
# #             return response.text
# #         except Exception as e:
# #             if attempt == retries - 1:
# #                 st.error(f"Error communicating with the API: {str(e)}")
# #                 raise
# #             time.sleep(1)

# # def input_image_setup(uploaded_file) -> List[Dict]:
# #     """Process uploaded image and return in format required by Gemini API."""
# #     if not uploaded_file:
# #         raise ValueError("Please upload an image.")
    
# #     try:
# #         image = Image.open(uploaded_file)
# #         if image.mode not in ('RGB', 'L'):
# #             image = image.convert('RGB')
# #         bytes_data = uploaded_file.getvalue()
# #         if len(bytes_data) > 4 * 1024 * 1024:
# #             raise ValueError("Image size too large. Upload an image smaller than 4MB.")
# #         return [{"mime_type": uploaded_file.type, "data": bytes_data}]
# #     except Exception as e:
# #         st.error(f"Error processing image: {str(e)}")
# #         return []

# # def generate_bio_prompt(base_mood: str, modifiers: List[str], custom_mood: str, num_bios: int) -> str:
# #     """Generate prompt for bio creation."""
# #     mood_description = base_mood
# #     if modifiers:
# #         mood_description += f" with elements of {', '.join(modifiers)}"
# #     if custom_mood:
# #         mood_description += f" and {custom_mood}"

# #     return f"""
# #     As an Instagram bio expert, create {num_bios} unique bios matching this mood: {mood_description}.

# #     Guidelines:
# #     - Each bio under 150 characters.
# #     - Use relevant emojis.
# #     - Make them catchy and memorable.
# #     - Match the mood and image.
# #     - Incorporate the specified modifiers.
# #     - Give only bio on each new line nothing else.
# #     """

# # def save_bio(supabase: Client, bio: str, user_id: str, is_favorite: bool = False):
# #     data = {
# #         "user_id": user_id,
# #         "bio": bio,
# #         "created_at": time.time(),
# #         "is_favorite": is_favorite
# #     }
# #     supabase.table("bios").insert(data).execute()

# # def get_favorite_bios(supabase: Client, user_id: str):
# #     response = supabase.table("bios").select("*").eq("user_id", user_id).eq("is_favorite", True).execute()
# #     return response.data

# # def get_bio_history(supabase: Client, user_id: str):
# #     response = supabase.table("bios").select("*").eq("user_id", user_id).execute()
# #     return response.data

# # def save_user(supabase: Client, email: str, user_id: str):
# #     data = {
# #         "email": email,
# #         "user_id": user_id,
# #         "created_at": time.time()
# #     }
# #     supabase.table("users").insert(data).execute()

# # def main():
# #     # Initialize API and Supabase client
# #     if not initialize_api():
# #         return
# #     supabase = initialize_supabase()

# #     st.markdown("<h1 style='text-align: center;'>✨ Instagram Bio Generator ✨</h1>", unsafe_allow_html=True)
# #     st.markdown("### Transform your photos into engaging Instagram bios!")

# #     # User authentication
# #     if 'user_id' not in st.session_state:
# #         st.subheader("Login / Signup")

# #         option = st.selectbox("Select an option:", ["Login", "Signup"])
# #         email = st.text_input("Email", placeholder="Enter your email")
# #         password = st.text_input("Password", type="password", placeholder="Enter your password")

# #         if option == "Signup":
# #             if st.button("Create Account"):
# #                 try:
# #                     user = supabase.auth.sign_up({"email": email, "password": password})
# #                     st.session_state['user_id'] = user.user.id  # Access user ID with dot notation
# #                     save_user(supabase, email, user.user.id)  # Save user info to database
# #                     st.success("Account created successfully! Please log in.")
# #                 except Exception as e:
# #                     st.error(f"Error creating account: {str(e)}")

# #         elif option == "Login":
# #             if st.button("Login"):
# #                 try:
# #                     user = supabase.auth.sign_in({"email": email, "password": password})
# #                     st.session_state['user_id'] = user.user.id  # Access user ID with dot notation
# #                     st.success("Logged in successfully!")
# #                     st.experimental_rerun()  # Redirect to main app after login
# #                 except Exception as e:
# #                     st.error(f"Error logging in: {str(e)}")

# #         return

# #     # Main app functionality after user is logged in
# #     uploaded_file = st.file_uploader("Upload your image (JPG, JPEG, or PNG)", type=["jpg", "jpeg", "png"], help="Max size: 4MB")

# #     st.markdown("### 🎨 Choose Your Vibe")

# #     col1, col2 = st.columns([2, 1])
# #     with col1:
# #         base_mood = st.selectbox("Select Base Mood", options=PRESET_MOODS)
# #         custom_mood = st.text_input("Add Custom Mood (optional)", placeholder="e.g., Wanderlust, Coffee lover")

# #         with st.expander("✨ Add Mood Modifiers", expanded=True):
# #             selected_modifiers = []
# #             for category, modifiers in MOOD_MODIFIERS.items():
# #                 st.write(f"**{category}**")
# #                 cols = st.columns(3)
# #                 for i, modifier in enumerate(modifiers):
# #                     with cols[i % 3]:
# #                         if st.checkbox(modifier, key=f"modifier_{modifier}"):
# #                             selected_modifiers.append(modifier)

# #     with col2:
# #         num_bios = st.number_input("How many bios to generate?", min_value=1, max_value=10, value=3)

# #     if uploaded_file and st.button("Generate Bios"):
# #         try:
# #             image_parts = input_image_setup(uploaded_file)
# #             prompt = generate_bio_prompt(base_mood, selected_modifiers, custom_mood, num_bios)
# #             bios = get_gemini_response(image_parts, prompt)
            
# #             # Display bios
# #             st.markdown("<h2>Your Generated Bios:</h2>", unsafe_allow_html=True)
# #             for bio in bios.splitlines():
# #                 st.markdown(f"<div class='bio-box'>{bio}</div>", unsafe_allow_html=True)
# #                 if st.button(f"⭐ Add to Favorites", key=bio):
# #                     save_bio(supabase, bio, st.session_state['user_id'], is_favorite=True)
# #                     st.success("Bio added to favorites!")

# #             if st.button("View Favorite Bios"):
# #                 favorites = get_favorite_bios(supabase, st.session_state['user_id'])
# #                 if favorites:
# #                     st.subheader("Your Favorite Bios:")
# #                     for favorite in favorites:
# #                         st.markdown(f"<div class='bio-box'>{favorite['bio']}</div>", unsafe_allow_html=True)
# #                 else:
# #                     st.warning("No favorite bios yet.")

# #         except Exception as e:
# #             st.error(f"An error occurred: {str(e)}")

# # if __name__ == "__main__":
# #     main()
