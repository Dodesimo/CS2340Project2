from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import google.generativeai as genai
from django.conf import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Gemini API
try:
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == 'your-api-key-here':
        raise ValueError("Gemini API key not properly configured")
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    logger.info("Gemini API initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Gemini API: {str(e)}")
    model = None

def index(request):
    """Render the main chat interface."""
    return render(request, 'chatbot/index.html')

@require_http_methods(["POST"])
def chat(request):
    """Handle chat messages and return AI responses."""
    if model is None:
        return JsonResponse({
            'error': 'Chatbot service is currently unavailable. Please try again later.'
        }, status=503)
    
    try:
        message = request.POST.get('message', '')
        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)
            
        response = model.generate_content(message)
        return JsonResponse({'response': response.text})
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return JsonResponse({
            'error': 'An error occurred while processing your request. Please try again later.'
        }, status=500)

def new_conversation(request):
    """Start a new conversation."""
    return JsonResponse({'status': 'success'})

def test_gemini(request):
    """Test the Gemini API connection."""
    if model is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Gemini API not properly configured'
        }, status=503)
        
    try:
        response = model.generate_content("Hello, this is a test message.")
        return JsonResponse({'status': 'success', 'response': response.text})
    except Exception as e:
        logger.error(f"Error in test_gemini endpoint: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def debug(request):
    """Debug endpoint for admin use."""
    return JsonResponse({
        'status': 'debug endpoint',
        'api_key_configured': bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != 'your-api-key-here'),
        'model_initialized': model is not None
    }) 