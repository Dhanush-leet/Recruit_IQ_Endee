import google.generativeai as genai
import os, json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_screening_analysis(prompt: str) -> dict:
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        return json.loads(text)
    except Exception as e:
        return {
            "recommendation": "ANALYSIS ERROR",
            "hire_reason": str(e),
            "concern": "Could not parse LLM response",
            "suggested_interview_questions": []
        }
