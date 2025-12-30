import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Module logger
logger = logging.getLogger(__name__)

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
        logger.error("GEMINI_API_KEY not found in environment variables.")
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
            logger.error("AI response did not contain 'score' or 'feedback'.")
            return None
    except Exception as e:
        logger.exception("An error occurred while calling the API or parsing the response")
        return None


def validate_and_generate_term(term: str, existing_terms: list):
    """
    Uses Gemini API to validate a user-suggested term and generate its content.
    
    Args:
        term: The term suggested by the user
        existing_terms: List of terms already in the database
        
    Returns:
        Dictionary with validation result and generated content, or None on error
        {
            "approved": bool,
            "reason": str,  # Why it was approved/rejected
            "category": str,  # One of the 17 categories
            "formal_definition": str,
            "simple_definition": str,
            "example": str,
            "why_it_matters": str,
            "difficulty": int  # 1-5
        }
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment variables.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    categories = [
        "devops", "docker-kubernetes", "ci-cd", "terraform", "ansible", 
        "aws", "azure", "networking", "security", "databases", 
        "system-design", "api-design", "git", "linux", 
        "cdn-caching", "agile-methodology", "swe"
    ]

    prompt = f"""
    You are an expert technical term curator for a software engineering, DevOps, cloud, and cybersecurity learning platform.

    **User's Suggested Term:**
    {term}

    **Existing Terms in Database (check for duplicates):**
    {', '.join(existing_terms[:50])}... (showing first 50)

    **Available Categories:**
    {', '.join(categories)}

    **Your Task:**
    1. Check if this term already exists in the database (STRICT fuzzy match - consider synonyms, abbreviations, similar meanings, etc.)
    2. Determine if it's relevant to software engineering, DevOps, cloud, networking, security, or system design
    3. Determine if it fits into one of the available categories
    4. If approved, generate comprehensive content for the term

    **CRITICAL - Duplicate Detection Rules:**
    - REJECT if the term is semantically identical to an existing term (e.g., "what is X" vs "What is X?")
    - REJECT if it's a rephrased version of an existing term
    - REJECT if the meaning is the same even if wording differs slightly
    - REJECT if only punctuation, capitalization, or minor wording differs
    - Example: "Docker vs Docker Compose" and "difference between Docker and Docker Compose" are THE SAME
    
    **Approval Criteria:**
    - NOT already in database (or semantically similar term)
    - Completely unique technical concept, not a rewording
    - Relevant to tech/software/DevOps/cloud/security domains
    - Fits into at least one of the available categories
    - Is a genuine technical concept, not slang or joke

    **IMPORTANT: Return ONLY valid JSON with this exact structure:**
    {{
        "approved": true/false,
        "reason": "Brief explanation of approval/rejection",
        "category": "one of the categories listed above (only if approved)",
        "formal_definition": "Academic/formal definition (only if approved)",
        "simple_definition": "Simple 1-sentence explanation (only if approved)",
        "example": "Real-world example or use case (only if approved)",
        "why_it_matters": "Why engineers should know this (only if approved)",
        "difficulty": 1-5 integer (only if approved, 1=beginner, 5=expert)
    }}

    If rejected, only include "approved", "reason", and set others to null.
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        result = json.loads(cleaned_response)
        
        required_keys = ["approved", "reason"]
        if not all(key in result for key in required_keys):
            logger.error("AI response missing required keys")
            return None
            
        return result
    except Exception as e:
        logger.exception("An error occurred while validating term")
        return None
        