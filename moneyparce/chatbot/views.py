from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import google.generativeai as genai
from django.conf import settings

# Initialize Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def index(request):
    """Render the main chat interface."""
    return render(request, 'chatbot/index.html')

@require_http_methods(["POST"])
def chat(request):
    """Handle chat messages and return AI responses."""
    try:
        message = request.POST.get('message', '')
        response = model.generate_content(message)
        return JsonResponse({'response': response.text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def new_conversation(request):
    """Start a new conversation."""
    return JsonResponse({'status': 'success'})

def test_gemini(request):
    """Test the Gemini API connection."""
    try:
        response = model.generate_content("Hello, this is a test message.")
        return JsonResponse({'status': 'success', 'response': response.text})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def debug(request):
    """Debug endpoint for admin use."""
    return JsonResponse({'status': 'debug endpoint'}) 