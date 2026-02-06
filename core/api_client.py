import requests
import json
import os
from dotenv import load_dotenv

# Loading variables from the .env file
load_dotenv()

def call_local_ai(instruction, code_context):
    """
    Connects to Ollama using settings from the .env file.
    """
    # Fetching settings from .env (with fallback)
    url = f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}/api/generate"
    model_name = os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:0.5b')
    
    full_prompt = f"### INSTRUCTION:\n{instruction}\n\n### CODE TO REVIEW:\n{code_context}\n\n### RESPONSE:"
    
    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('response', "AI returned empty text.")
        else:
            return f"⚠️ Ollama Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
# TEST BLOCK to see if api_client working properly 
if __name__ == "__main__":
    print("Testing the Bridge...")
    test_code = "print('Hello World')"
    test_job = "Explain what this code does and tell me a fun fact about Python and tell us which is better java or python"
    
    result = call_local_ai(test_job, test_code)
    print("\n--- AI RESPONSE ---")
    print(result)