# formdata/views.py
from django.shortcuts import redirect, render
import time

# Create your views here.
def show_form(request):
    """
        show the HTML form to the client
    """

    # use this template to produce the response
    template_name = "formdata/form.html"

    context = {
        "current_time": time.ctime(),
    }

    return render(request, template_name, context)


def submit(request):
    '''Process the form submission, and generate a result.'''
    template_name = "formdata/confirmation.html"
    
    # Only process if the request method is POST
    if request.method == 'POST':
        # Read the form data into python variables
        name = request.POST.get('name', '')
        favorite_color = request.POST.get('favorite_color', '')
        
        context = {
            'name': name,
            'favorite_color':  favorite_color,
            "current_time": time.ctime(),
        }
        
        return render(request, template_name, context)
    
    # If the request method is not POST, redirect back to the form
    return redirect('show_form')