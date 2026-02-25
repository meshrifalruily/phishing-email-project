from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
from transformers import pipeline
from huggingface_hub import login 
import torch
from dotenv import load_dotenv
import os 

print(torch.backends.mps.is_available())
print(torch.__version__)

load_dotenv()
login(token=os.environ["hf_token"])

from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "Auguzcht/securisense-phishing-detection"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)

# print("Downloaded successfully")
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="Auguzcht/securisense-phishing-detection",
    device="mps"
)

email = "Dear user, your account will be suspended. Click here to verify."

result = classifier(email)

print(result)