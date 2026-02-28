from openai import OpenAI
import torch 
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=os.getenv("openrouter_api_key")
    #api_key= settings.openrouter_api_key
)

def generate_text(prompt: str) -> str:
    """
    Analyzes email content using OpenRouter's AI model.
    
    Args:
        prompt (str): The email content to analyze
        
    Returns:
        str: AI analysis of the email
    """
    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-nano-30b-a3b:free",
            messages=[
                {"role": "system", "content": 'You are a cybersecurity expert.'
                ' Analyze the following email and determine if it is Phishing '
                'or Safe. Explain your reasoning with confidence percentages.'},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = f"Error connecting to OpenRouter API: {str(e)}\n\n"
        error_message += "Please check:\n"
        error_message += "1. Your internet connection\n"
        error_message += "2. Your openrouter_api_key in .env file\n"
        error_message += "3. OpenRouter API status\n\n"
        error_message += f"Error details: {type(e).__name__}"
        return error_message
