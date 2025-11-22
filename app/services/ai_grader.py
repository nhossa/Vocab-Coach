import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

def grade_user_answer(term: str, correct_definition: str, user_answer: str):
    """
    Uses the Gemini API to grade a user's answer for a technical term.

    Args:
        term: The technical term being quizzed.
        correct_definition: The ideal answer/definition.
        user_answer: The user's submitted answer.

    Returns:
        A dictionary containing the 'score' and 'feedback', or None on error.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an expert AI assistant for software, devops, cloud, cybersecurity, system, and network engineers. Your task is to evaluate a user's explanation of a technical term and provide a score and constructive feedback.

    **Technical Term:**
    {term}

    **Correct Definition:**
    {correct_definition}

    **User's Answer:**
    {user_answer}

    **Instructions:**
    1. Compare the "User's Answer" to the "Correct Definition".
    2. Evaluate the user's answer on a scale from 0 to 100 based on accuracy and completeness.
    3. Provide clear, constructive feedback that helps the user learn. The feedback should highlight strengths and weaknesses.
    4. Return your evaluation in a strict JSON format with two keys: "score" (an integer) and "feedback" (a string).

    **IMPORTANT: Your entire response must be only the raw JSON object, with no extra text or formatting.**
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        result = json.loads(cleaned_response)
        if "score" in result and "feedback" in result:
            return result
        else:
            print("Error: AI response did not contain 'score' or 'feedback'.")
            return None
    except Exception as e:
        print(f"An error occurred while calling the API or parsing the response: {e}")
        