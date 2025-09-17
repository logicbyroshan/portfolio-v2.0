# ai/views.py
from django.http import JsonResponse
from django.views import View
import json
import logging
from .models import AIQuery
from .llm_utills import ask_gemini
from .utils import get_portfolio_context

logger = logging.getLogger(__name__)

class AIQuerySubmitView(View):
    """
    Handles the submission of the AI query form with real-time AI responses.
    """
    def get(self, request, *args, **kwargs):
        # This endpoint only accepts POST requests
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    def post(self, request, *args, **kwargs):
        try:
            # Get the question from POST data
            question_text = request.POST.get('question', '').strip()
            attached_file = request.FILES.get('attachment')

            # Debug logging
            logger.info(f"Received question: '{question_text}'")
            logger.info(f"Content type: {request.content_type}")
            logger.info(f"POST data keys: {list(request.POST.keys())}")
            logger.info(f"FILES data keys: {list(request.FILES.keys())}")

            if not question_text:
                logger.warning("Empty question received")
                return JsonResponse({
                    'success': False,
                    'status': 'error', 
                    'message': 'A question is required.'
                }, status=400)

            # Save the query to database
            AIQuery.objects.create(
                question=question_text,
                attachment=attached_file
            )
            
            # Get AI response using Gemini
            portfolio_data = get_portfolio_context()
            
            prompt = f"""
{portfolio_data}

## Current User Question: 
"{question_text}"

## Response Instructions:
- Respond as Roshan Damor in first person (use "I", "my", "me")
- Be enthusiastic and professional
- For job/project opportunities: ALWAYS say "Yes, I'd love to work on this!"
- Always encourage direct contact for further discussion
- Keep responses focused on the context provided above
- If question is outside my expertise, politely redirect to my core skills
"""
            
            ai_response = ask_gemini(prompt)
            
            return JsonResponse({
                'success': True, 
                'response': ai_response,
                'message': 'Query processed successfully.'
            })
            
        except Exception as e:
            # Log the error (should use proper logging in production)
            logger.error(f"Error in AIQuerySubmitView: {str(e)}")
            return JsonResponse({
                'success': False,
                'response': 'Sorry, I encountered an error processing your request. Please try again.',
                'message': 'An internal error occurred.'
            }, status=500)