from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from openrouter import generate_text
from phishing import analyze_email

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze_email", response_class=HTMLResponse)
async def analyze_email_endpoint(request: Request, email: str = Form(...)):
 
    if not email:
        return templates.TemplateResponse("index.html", {"request": request})
    
    openrouter_result = generate_text(email)
    hf_result = analyze_email(email)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "email": email,
        "openrouter_analysis": openrouter_result,
        "label": hf_result['label'],
        "score": hf_result['score']
    })