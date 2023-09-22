from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User


import os
from os.path import join, dirname
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.path.dirname(BASEDIR)
BASEDIR = os.path.dirname(BASEDIR)

dotenv_path = join(BASEDIR, '.env')
load_dotenv(dotenv_path)

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = openai_api_key

def ask_openai(message):
  response = openai.Completion.create(
    model = "text-davinci-003",
    prompt = message,
    max_tokens = 50,
    n=1,
    stop=None,
    temperature=0.7,
  )

  print(response)
  answer = response.choices[0].text.strip()
  print(answer)
  return answer

# Create your views here.
def chatbot(request):
  if request.method == 'POST':
    message = request.POST.get('message')
    response = ask_openai(message)
    return JsonResponse({'message': message, 'response': response})
  return render(request, 'chatbot.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return redirect('chatbot')
    else:
      error_message = "INVALID USERNAME OR PASSWORD"
      return render(request, 'login.html', {'error_message': error_message})
  else:
    return render(request, 'login.html')


def register(request):
  if request.method == "POST":
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    if password1 == password2:
      try:
        user = User.objects.create_user(username, email, password1)
        user.save()
        auth.login(request, user)
        return redirect('chatbot')
      except:
        error_message = "ERROR CREATING ACCOUNT"
        return render(request, 'register.html', {'error_message': error_message})
    else:
      error_message = "PASSWORDS DO NOT MATCH"
      return render(request, 'register.html', {'error_message': error_message})

  return render(request, 'register.html')


def logout(request):
  auth.logout(request)