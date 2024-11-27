import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables securely
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


# Configure the LLM API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash",generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 500,
})

def generate_response(prompt):
    try:
        # Use the correct method to generate text
        response = model.generate_content(
            prompt,
        )
        return response.text if response.text else "No response generated."
    except Exception as e:
        return f"An error occurred while processing your request: {e}"
