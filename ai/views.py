# ai/views.py
from django.http import JsonResponse
from django.views import View
from .models import AIQuery

class AIQuerySubmitView(View):
    """
    Handles the submission of the AI query form.
    """
    def get(self, request, *args, **kwargs):
        # This endpoint only accepts POST requests
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

    def post(self, request, *args, **kwargs):
        question_text = request.POST.get('question')
        attached_file = request.FILES.get('attachment')

        if not question_text or question_text.strip() == '':
            return JsonResponse({'status': 'error', 'message': 'A question is required.'}, status=400)

        try:
            AIQuery.objects.create(
                question=question_text,
                attachment=attached_file
            )
            return JsonResponse({'status': 'success', 'message': 'Thank you! Your query has been submitted.'})
        except Exception as e:
            # Log the error for debugging
            print(f"Error saving AI Query: {e}")
            return JsonResponse({'status': 'error', 'message': 'An internal error occurred.'}, status=500)