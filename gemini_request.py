import google.generativeai as genai
import user_config

# Configure Gemini
genai.configure(api_key=user_config.GEMINI_API_KEY)

# Basic Gemini request
def generate_from_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("[Gemini Error]", e)
        return None

# For role-based chat
def send_request2(chat_history):
    try:
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(chat_history[-1]['content'])
        return response.text
    except Exception as e:
        print("[Gemini Chat Error]", e)
        return None
    
    