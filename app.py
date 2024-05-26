import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("api_key")

# Set up Google Gemini-Pro AI model
genai.configure(api_key=GOOGLE_API_KEY)

# Load gemini-pro model
def gemini_pro():
    model = genai.GenerativeModel('gemini-pro')
    return model

# Load gemini vision model
def gemini_vision():
    model = genai.GenerativeModel('gemini-pro-vision')
    return model

# Load gemini-pro-code model
def gemini_pro_code():
    model = genai.GenerativeModel('gemini-pro-code')
    return model

# get response from gemini pro vision model
def gemini_vision_response(model, prompt, image):
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Set page title and icon
st.set_page_config(
    page_title="Chat With Gemi",
    page_icon="✌️✌️",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    user_picked = option_menu(
        "Google Gemini AI",
        ["ChatBot", "Image Captioning", "Code Generation"],
        menu_icon="robot",
        icons = ["chat-dots-fill", "image-fill", "code-slash"],
        default_index=0
    )

def roleForStreamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

if user_picked == 'ChatBot':
    model = gemini_pro()
    
    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = model.start_chat(history=[])

    st.title("🤝Say something, I can answer you")

    # Display the chat history
    for message in st.session_state.chat_history.history:
        with st.chat_message(roleForStreamlit(message.role)):    
            st.markdown(message.parts[0].text)

    # Get user input
    user_input = st.chat_input("Message TalkBot:")
    if user_input:
        st.chat_message("user").markdown(user_input)
        try:
            response = st.session_state.chat_history.send_message(user_input)
            with st.chat_message("assistant"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

elif user_picked == 'Image Captioning':
    model = gemini_vision()

    st.title("🙌Image Captioning")

    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    user_prompt = st.text_input("Enter the prompt for image captioning:")

    if st.button("Generate Caption"):
        if image is None:
            st.error("Please upload an image first.")
        else:
            load_image = Image.open(image)

            colLeft, colRight = st.columns(2)

            with colLeft:
                st.image(load_image.resize((800, 500)))

            caption_response = gemini_vision_response(model, user_prompt, load_image)

            with colRight:
                if "Error" in caption_response:
                    st.error(caption_response)
                else:
                    st.info(caption_response)

elif user_picked == 'Code Generation':
    model = gemini_pro_code()  # Use the new function
    st.title("💻Code Generation")

    code_prompt = st.text_area("Enter your code prompt:")
    
    # Example prompts
    st.markdown("**Example Prompts:**")
    st.markdown("- Write a Python function to reverse a string.")
    st.markdown("- Create a JavaScript function that checks if a number is prime.")
    st.markdown("- Generate a simple HTML page with a button.")

    if st.button("Generate Code"):
        if not code_prompt:
            st.warning("Please enter a code prompt.")
        else:
            try:
                response = model.generate_text(code_prompt, temperature=0.2, max_output_tokens=500)
                st.code(response.text, language="python")  # Assume Python for now
            except Exception as e:
                st.error(f"Error: {e}")