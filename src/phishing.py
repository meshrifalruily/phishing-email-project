from transformers import pipeline
from huggingface_hub import login 
import torch
from dotenv import load_dotenv
import os 

print(torch.backends.mps.is_available())
print(torch.__version__)

load_dotenv()
login(token=os.environ["hf_token"])

classifier = pipeline(
    "text-classification",
    model="Auguzcht/securisense-phishing-detection",
    device="mps", 
)

def analyze_email(email: str):
    """
    Analyzes email content for phishing detection.
    
    Args:
        email (str): The email content to analyze
        
    Returns:
        list: Classification results with labels and scores
    """
    if not email or not email.strip():
        return [{"label": "LABEL_0", "score": 0.0}]
    
    result = classifier(email)
    return result[0]

print(analyze_email("Congratulations! You've won a free iPhone. Click here to claim your prize."))  

