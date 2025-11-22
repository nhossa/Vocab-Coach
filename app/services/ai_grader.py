import os
import json
from dotenv import load_dotenv
import google.generativeai as genai


# We will call this function from our quiz router
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
    # Load environment variables from .env file
    load_dotenv()

    # --- 1. Get API Key and Configure Gemini ---
    # This reads the key you just saved in your .env file.
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return None

    try:
        # Configure the Gemini library with your key
        genai.configure(api_key=api_key)
        # Create an instance of the generative model
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return None

    # --- 2. Create the Prompt for the AI ---
    # This is the detailed instruction we send to the AI.
    # We tell it what its role is, what information to use, and how to format the output.
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

    # --- 3. Call the API and Parse the Response ---
    try:
        # Send the prompt to the AI
        generation_config = {
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
        response = model.generate_content(prompt, generation_config=generation_config)

        # Pull text safely even if the SDK shape changes
        raw_text = getattr(response, "text", None)
        if not raw_text and getattr(response, "candidates", None):
            first_candidate = response.candidates[0]
            parts = getattr(first_candidate, "content", None)
            if parts and getattr(parts, "parts", None):
                raw_text = "".join(
                    part.text for part in parts.parts if getattr(part, "text", None)
                )

        if not raw_text:
            print("Error: Empty response from Gemini.")
            return None

        # The response text might have markdown formatting (like ```json); clean it.
        cleaned_response = raw_text.strip().replace('```json', '').replace('```', '')

        # Parse the JSON string into a Python dictionary
        result = json.loads(cleaned_response)
        print(result)

        # Make sure the AI gave us the keys we asked for
        if "score" in result and "feedback" in result:
            return result
        else:
            print("Error: AI response did not contain 'score' or 'feedback'.")
            return None

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}. Raw response: {raw_text}")
        return None
    except Exception as e:
        print(f"An error occurred while calling the API or parsing the response: {e}")
        return None
