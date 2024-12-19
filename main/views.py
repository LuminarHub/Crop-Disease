from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,CreateView
from .disease_prediction import *
from django.http import JsonResponse
from groq import Groq
import json
from social_core.exceptions import AuthCanceled
from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout,authenticate,login
from .models import *
from django.urls import reverse_lazy
from .forms import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class CustomLogoutView(View):
    def get(self, request):
        logout(request)  # Log out the user
        response = redirect('/')  # Redirect to home or login page
        response.delete_cookie('sessionid')  # Delete session cookie
        response.delete_cookie('csrftoken')  # Delete CSRF token if applicable
        return response

def custom_social_auth_exception_middleware(request, exception):
    if isinstance(exception, AuthCanceled):
        return redirect('login')
    return render(request, 'error.html', {'error': str(exception)})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        log_form=LogForm(data=request.POST)
        if log_form.is_valid():  
            email=log_form.cleaned_data.get('email')
            password=log_form.cleaned_data.get('password')
            user=authenticate(request,email=email,password=password)
            print(user)
            if user: 
                login(request,user)
                return redirect('home')
            else:
                return render(request,'login.html',{"form":log_form})
        else:
            return render(request,'login.html',{"form":log_form}) 
    return render(request, 'login.html')

class Home(TemplateView):
    template_name='home.html'

class SchemeView(TemplateView):
    template_name='schemes.html'


class ChatbotView(View):
    def get(self, request):
        return render(request, "chatbot.html")
    def post(self, request): 
        try:
            body = json.loads(request.body)
            user_input = body.get('userInput')
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format."})
    
        if not user_input:  # If user_input is None or empty
            print("no")
            return JsonResponse({"error": "No user input provided."})  
        
        print("User Input:", user_input)
        
        static_responses = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! How can I help you?",
            "how are you": "I'm just a chatbot, but I'm doing great! How about you?",
            "bye": "Goodbye! Take care.",
            "whats up": "Not much, just here to help you with SNGCE queries. How can I help you today?",
        }

        lower_input = user_input.lower().strip()
        if lower_input in static_responses:
            print(static_responses[lower_input])
            return JsonResponse({'response': static_responses[lower_input]})
        
        try:
            print("Processing via GROQ")
            data = get_groq_response(user_input)
            return JsonResponse({'response': data})
        except Exception as e:
            return JsonResponse({"error": f"Failed to get GROQ response: {str(e)}"})



def get_groq_response(user_input):
    """
    Communicate with the GROQ chatbot to get a response based on user input.
    """
    print("user input:", user_input)
    
    client = Groq(
        api_key="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",
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,  # Use the user input here
            }
        ],
        model="llama3-8b-8192",
        stream=False,
    )

    response = chat_completion.choices[0].message.content
    return response



class PredictionView(View):
    def get(self, request):
        return render(request, "disease_prediction.html")
    def post(self, request):
        image = request.FILES.get('image')     
        if not image:
            return render(request, "prediction.html", {'error': 'Please upload an image.'})
        test_image = load_and_prep_image(image, img_shape=128)
        cat=predicted_class(class_labels,model_path,test_image)
        return render(request,"disease_prediction.html",{'response': cat})
    



class RegView(CreateView):
    form_class=Reg
    template_name="signup.html"
    model=CustUser
    success_url=reverse_lazy("login")  