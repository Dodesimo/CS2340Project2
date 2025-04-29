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
    model = genai.GenerativeModel('gemini-1.5-pro')
    logger.info("Gemini API initialized successfully")
except Exception as e:
    logger.error(f"Error initializing Gemini API: {str(e)}")
    model = None

def index(request):
    """Render the main chat interface."""
    # Retrieve chat history from session or initialize if not present
    messages = request.session.get('chat_messages', [])
    import json
    messages_json = json.dumps(messages)
    return render(request, 'chatbot/index.html', {
        'messages': messages,
        'messages_json': messages_json
    })

import json # Add json import

@require_http_methods(["POST"])
def chat(request):
    """Handle chat messages and return AI responses based on mode."""
    if model is None:
        return JsonResponse({
            'error': 'Chatbot service is currently unavailable. Please configure the API key.'
        }, status=503)

    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        message = data.get('message', '')
        mode = data.get('mode', 'general') # Default to general chat

        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Construct prompt based on mode
        if mode == 'financial_advice':
            prompt = f"Provide financial advice based on the following user query: '{message}'. Focus on actionable steps and general financial principles. Do not give specific investment recommendations."
        elif mode == 'budget_tutorial':
            prompt = f"Act as a budgeting tutor. Explain the concept or answer the question related to budgeting based on the user's query: '{message}'. Keep the explanation clear and simple."
        else: # General mode
            prompt = message

        logger.info(f"Sending prompt to Gemini (mode: {mode}): {prompt[:100]}...") # Log prompt
        response = model.generate_content(prompt)
        logger.info(f"Received response from Gemini: {response.text[:100]}...") # Log response

        # Retrieve chat history from session or initialize
        messages = request.session.get('chat_messages', [])
        # Append user message
        messages.append({'is_user': True, 'content': message})
        # Append AI response
        messages.append({'is_user': False, 'content': response.text})
        # Save back to session
        request.session['chat_messages'] = messages
        request.session.modified = True

        return JsonResponse({'response': response.text})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    except Exception as e:
        logger.error(f"Error in chat endpoint (mode: {mode}): {str(e)}")
        return JsonResponse({
            'error': 'An error occurred while processing your request. Please try again later.'
        }, status=500)

def new_conversation(request):
    """Start a new conversation."""
    # Clear chat history in session
    request.session['chat_messages'] = []
    request.session.modified = True
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