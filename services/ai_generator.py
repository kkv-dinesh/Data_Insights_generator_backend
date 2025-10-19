# ai_generator.py
import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# Initialize client
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_insights(statistical_facts: dict) -> str:
    """
    Generates a concise AI textual summary report from statistical facts.
    """
    if not statistical_facts:
        return "No numerical data found for analysis."

    facts_string = ""
    for col, vals in statistical_facts.items():
        facts_string += (
            f"- {col} ({vals.get('dtype')}): Count={vals.get('count')}, "
            f"Mean={vals.get('mean')}, Median={vals.get('median')}, "
            f"Mode={vals.get('mode')}, Std Dev={vals.get('std_dev')}, "
            f"Min={vals.get('min')}, Max={vals.get('max')}"
        )
        if vals.get("has_pie"):
            facts_string += " | Pie chart generated."
        facts_string += "\n"

    prompt_text = (
        "You are an expert data analyst. Generate a concise textual summary of the "
        "dataset with bullet points for each column, highlighting key trends, outliers, "
        "missing values, and distribution patterns. Make it professional, easy to read, "
        "and suitable for a report.\n\n"
        f"{facts_string}\n"
    )

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=[prompt_text]
        )
        return response.text
    except Exception as e:
        print(f"AI generation error: {e}")
        return "An error occurred while generating AI insights."
