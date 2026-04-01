# Phishing Email Detector

A FastAPI-based web application that analyzes email content for potential phishing threats using a combination of specialized machine learning models and Large Language Models (LLMs).

## Project Overview
This project provides a web interface where users can paste email content to receive a dual-layered security analysis:
1.  **Classification Analysis:** Uses a dedicated phishing detection model from HuggingFace (`Auguzcht/securisense-phishing-detection`) to provide a confidence score and label (Phishing vs. Safe).
2.  **Expert Reasoning:** Utilizes OpenRouter (specifically `nvidia/nemotron-3-nano-30b-a3b:free`) to provide a detailed cybersecurity expert's perspective on why an email might be malicious.

## Key Technologies
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Templating:** [Jinja2](https://jinja.palletsprojects.com/)
- **AI/ML:**
    - [Transformers](https://huggingface.co/docs/transformers/index) (HuggingFace)
    - [OpenRouter API](https://openrouter.ai/) (OpenAI-compatible client)
- **Utilities:** `python-dotenv` for environment management, `uvicorn` as the ASGI server.

## Building and Running

### Prerequisites
- Python 3.8+
- A HuggingFace API Token (with access to the required model)
- An OpenRouter API Key

### Installation
1.  **Virtual Environment:**
    ```bash
    # Create environment
    python -m venv env
    # Activate environment
    source env/bin/activate  # macOS/Linux
    .\env\Scripts\activate   # Windows
    ```
2.  **Dependencies:**
    ```bash
    pip install -r src/requirements.txt
    ```

### Configuration
Create a `.env` file in the project root with the following variables:
```env
hf_token=your_huggingface_token
openrouter_api_key=your_openrouter_api_key
```

### Running the Application
From the project root, run:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uvicorn main:app --reload --app-dir src
```
Alternatively, navigate to the `src` directory and run:
```bash
uvicorn main:app --reload
```
The application will be available at `http://localhost:8000`.

## Directory Structure
- `src/`: Core source code.
    - `main.py`: FastAPI application entry point and routing.
    - `phishing.py`: HuggingFace model integration for classification.
    - `openrouter.py`: LLM integration for expert analysis.
    - `templates/`: HTML templates for the web UI.
- `env/`: Python virtual environment (ignored by git).

## Development Conventions
- **Modular Logic:** AI integration is decoupled from web routing. Keep model-specific logic in `phishing.py` or `openrouter.py`.
- **Environment Variables:** Never hardcode API keys. Always use the `.env` file and `load_dotenv()`.
- **Styling:** The project uses embedded CSS in HTML templates for simplicity in this prototype.
- **Hardware Acceleration:** `phishing.py` is configured to use `mps` (Metal Performance Shaders) for macOS GPU acceleration if available.
