import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def list_available_models():
    """
    List available Gemini models for debugging purposes.
    """
    try:
        if not hasattr(settings, "GEMINI_API_KEY") or not settings.GEMINI_API_KEY:
            return []

        genai.configure(api_key=settings.GEMINI_API_KEY)
        models = []

        for model in genai.list_models():
            if "generateContent" in model.supported_generation_methods:
                models.append(model.name)
                logger.info(f"Available model: {model.name}")

        return models
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        return []


def ask_gemini(prompt):
    """
    Ask Gemini AI a question and return the response.
    """
    try:
        # Check if API key is configured
        if not hasattr(settings, "GEMINI_API_KEY") or not settings.GEMINI_API_KEY:
            logger.error("Gemini API key not configured")
            return "I'm sorry, but the AI service is not properly configured. Please contact the administrator."

        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # First, try to get list of available models
        available_models = []
        try:
            for model in genai.list_models():
                if "generateContent" in model.supported_generation_methods:
                    available_models.append(model.name)
                    logger.info(f"Available model: {model.name}")
        except Exception as list_error:
            logger.warning(f"Could not list models: {str(list_error)}")

        # Try different model names in order of preference
        # Using full model paths as returned by list_models()
        model_names = [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "models/gemini-pro",
            "models/gemini-1.0-pro",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro",
        ]

        # If we got available models, use those first
        if available_models:
            model_names = available_models + model_names

        model = None
        used_model_name = None

        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                used_model_name = model_name
                logger.info(f"Successfully initialized model: {model_name}")
                break
            except Exception as model_error:
                logger.warning(
                    f"Failed to initialize model {model_name}: {str(model_error)}"
                )
                continue

        if not model:
            logger.error("Failed to initialize any Gemini model")
            logger.error(f"Tried models: {model_names}")
            return "I'm sorry, but I'm having trouble connecting to the AI service. Please try again later."

        # Generate response
        response = model.generate_content(prompt)

        if response and response.text:
            logger.info(
                f"Successfully generated response using model: {used_model_name}"
            )
            return response.text
        else:
            logger.warning("Empty response from Gemini API")
            return "I apologize, but I couldn't generate a response. Please try again."

    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        return "I'm experiencing technical difficulties. Please try again later."
