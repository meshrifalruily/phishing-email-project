import os
import logging
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from openrouter import generate_text
from phishing import analyze_email

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure templates directory is correctly resolved relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI(title="Phishing Detector API")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze_email", response_class=HTMLResponse)
def analyze_email_endpoint(request: Request, email: str = Form(...)):
    """
    Synchronous endpoint to handle blocking AI analysis calls in a threadpool.
    """
    if not email or not email.strip():
        logger.warning("Empty email content submitted.")
        return templates.TemplateResponse("index.html", {"request": request})
    
    logger.info(f"Analyzing email content (Length: {len(email)})")
    
    try:
        # These are synchronous blocking calls, handled by FastAPI's threadpool
        openrouter_result = generate_text(email)
        hf_result = analyze_email(email)

        logger.info(f"Analysis complete. Label: {hf_result.get('label')}, Score: {hf_result.get('score')}")

        return templates.TemplateResponse("results.html", {
            "request": request,
            "email": email,
            "openrouter_analysis": openrouter_result,
            "label": hf_result.get('label', 'UNKNOWN'),
            "score": hf_result.get('score', 0.0)
        })
    except Exception as e:
        logger.error(f"Error processing analysis: {str(e)}", exc_info=True)
        return templates.TemplateResponse("results.html", {
            "request": request,
            "email": email,
            "openrouter_analysis": f"An error occurred during analysis: {str(e)}",
            "label": "ERROR",
            "score": 0.0
        })