from django.shortcuts import render
from django.http import JsonResponse
import openai

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