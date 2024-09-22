# hw/views.py
# the logic to handle URL requests
import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time

# Create your views here.
# def home(request):
#     '''
#         A function to respond to the /hw URL
#     '''

#     # create some text
#     response_text = f'''
#     <html>
#         <h2>Hello</h2>
#         <p>Hello World</p>
#         <hr>
#         This page was generate at {time.ctime()}.
#     '''

#     # return a response to the client
#     return HttpResponse(response_text)

def home(request):
    '''
        A function to respond to the /hw URL
        This function will delegate work to an HTML template
    '''

    template_name = "hw/home.html"
    context = {
        "current_time": time.ctime(),
        "letter1": chr(random.randint(65, 90)),
        "letter2": chr(random.randint(65, 90)),
        "number": random.randint(1, 10),
    }

    # delegate response to the template:
    return render(request, template_name, context)


def about(request):
    '''
        A function to respond to the /hw URL
        This function will delegate work to an HTML template
    '''

    template_name = "hw/about.html"
    context = {
        "current_time": time.ctime(),
    }

    # delegate response to the template:
    return render(request, template_name, context)