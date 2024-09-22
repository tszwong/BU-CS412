# quotes/views.py
# the logic to handle URL requests
import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time

# Create your views here.

quotes = [
    "I feel like people are expecting me to fail; therefore, I expect myself to win.",
    "You just need to be accepted for who you are and be proud of who you are and that is what I'm trying to do.",
    "Everyone has complicated lives, but the more you can simplify it and make it work for you, the better it is going to be."
]

img_urls = [
    "https://www.si.com/.image/t_share/MjAwODgyOTY5NjU5OTA5MzI0/m393390.jpg",
    "https://i.dailymail.co.uk/1s/2024/07/07/16/87037029-13609207-image-a-10_1720366965217.jpg",
    "https://media.formula1.com/image/upload/t_16by9Centre/f_auto/q_auto/v1719061595/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-1285771774.jpg"
]

def home(request):
    '''
        A function to respond to the /quotes URL
        This function will delegate work to an HTML template
    '''

    # pick random quote and img to be displayed
    curr_quote = random.choice(quotes)
    curr_image = random.choice(img_urls)

    template_name = "quotes/home.html"
    context = {
        "current_time": time.ctime(),
        "quote": curr_quote,
        "img_url": curr_image,
    }

    # delegate response to the template:
    return render(request, template_name, context)


def about(request):
    '''
        A function to respond to the /quotes URL
        This function will delegate work to an HTML template
    '''

    template_name = "quotes/about.html"
    context = {
        "current_time": time.ctime(),
    }

    # delegate response to the template:
    return render(request, template_name, context)


def quote(request):
    '''
        A function to respond to the /quotes URL
        This function will delegate work to an HTML template
    '''

    # pick random quote and img to be displayed
    curr_quote = random.choice(quotes)
    curr_image = random.choice(img_urls)

    template_name = "quotes/home.html"
    context = {
        "current_time": time.ctime(),
        "quote": curr_quote,
        "img_url": curr_image,
    }

    # delegate response to the template:
    return render(request, template_name, context)


def show_all(request):
    '''
        A function to respond to the /quotes URL
        This function will delegate work to an HTML template
    '''

    template_name = "quotes/show_all.html"
    context = {
        "current_time": time.ctime(),
        "all_quotes": quotes,
        "all_images": img_urls
    }

    # delegate response to the template:
    return render(request, template_name, context)