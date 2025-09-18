# beacon-project/backend/main_app/views.py
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the.env file
load_dotenv()

# Configure the Gemini API with your key
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    # This will help you debug if the API key is missing
    print(f"Error configuring Gemini API: {e}")
    model = None

@api_view()
def signup(request):
    """
    Handles user registration with a phone number and name.
    """
    try:
        phone_number = request.data.get('phone_number')
        name = request.data.get('name')
        
        if not phone_number or not name:
            return Response({'error': 'Phone number and name are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Using a dummy password for hackathon purposes
        password = 'demo_password_123'

        if User.objects.filter(username=phone_number).exists():
            return Response({'error': 'User with this phone number already exists'}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=phone_number, password=password)
        user.first_name = name
        user.save()

        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view()
def login(request):
    """
    Handles user login authentication.
    """
    try:
        phone_number = request.data.get('phone_number')
        # Using a dummy password for hackathon purposes
        password = 'demo_password_123'

        user = authenticate(request, username=phone_number, password=password)
        
        if user is not None:
            return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view()
def chatbot_response(request):
    """
    Handles chatbot interaction and sends the user message to the Gemini API.
    """
    try:
        user_message = request.data.get('message')

        if not user_message:
            return Response({'error': 'No message provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Define your AI agent's "persona"
        prompt = f"""
        You are a helpful and knowledgeable AI agent named BEACON. Your purpose is to assist Indian citizens with their government scheme applications.
        You are an expert on schemes for farmers.
        A user has messaged you. Your goal is to guide them, ask for their required details for the "Farmer Pension Scheme", check their eligibility, and then confirm that you will "auto-fill the form" for them.
        Do not actually fill a form. Your job is to act as the agent.
        
        User's message: {user_message}
        
        Your response:
        """

        # Generate a response from the Gemini model
        if model:
            response = model.generate_content(prompt)
            bot_response = response.text
            return Response({'response': bot_response}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Gemini API not configured'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)