from transformers import pipeline
from huggingface_hub import login 
import torch
from dotenv import load_dotenv
import os 
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize HuggingFace token
hf_token = os.getenv("hf_token")
if hf_token:
    login(token=hf_token)
else:
    logger.warning("hf_token not found in environment variables.")

# Dynamic device selection
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

logger.info(f"Using device: {device} for phishing detection model.")

# Initialize the classifier pipeline
try:
    classifier = pipeline(
        "text-classification",
        model="Auguzcht/securisense-phishing-detection",
        device=device, 
    )
except Exception as e:
    logger.error(f"Failed to load the model: {e}")
    classifier = None

def analyze_email(email: str):
    """
    Analyzes email content for phishing detection.
    
    Args:
        email (str): The email content to analyze
        
    Returns:
        dict: Classification results with label and score
    """
    if not classifier:
        return {"label": "ERROR", "score": 0.0}
        
    if not email or not email.strip():
        return {"label": "LABEL_0", "score": 0.0}
    
    try:
        result = classifier(email)
        return result[0]
    except Exception as e:
        logger.error(f"Error during classification: {e}")
        return {"label": "ERROR", "score": 0.0}

