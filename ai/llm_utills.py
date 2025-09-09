import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def ask_gemini(prompt):
    """
    Ask Gemini AI a question and return the response.
    """
    try:
        # Check if API key is configured
        if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
            logger.error("Gemini API key not configured")
            return "I'm sorry, but the AI service is not properly configured. Please contact the administrator."
        
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model name
        
        # Generate response
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "I apologize, but I couldn't generate a response. Please try again."
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        return "I'm experiencing technical difficulties. Please try again later."
