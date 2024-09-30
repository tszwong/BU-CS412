# restaurant/views.py
import datetime
import random
from django.shortcuts import redirect, render
import time

# Create your views here.
def main(request):
    """
        show the main web page to the client
    """

    # use this template to produce the response
    template_name = "restaurant/main.html"

    context = {
        "current_time": time.ctime(),
    }

    return render(request, template_name, context)


def order(request):
    """
        the food ordering page, which will display the order form
    """

    # use this template to produce the response
    template_name = "restaurant/order.html"

    daily_specials = [
        {"name": "Cindy's Chicken Wings", "price": 14.99, "description": "Crispy fried chicken wings made with our signature in-house Cindy Sauce"},
        {"name": "Tomato Egg Stir-fry", "price": 12.99, "description": "A simple yet flavorful dish featuring soft scrambled eggs stir-fried with juicy, tangy tomatoes. This classic Chinese comfort food is both savory and slightly sweet, perfect to enjoy with a bowl of steamed rice."},
        {"name": "Stir-Fried Baby Bok Choy", "price": 10.99, "description": "Tender and crisp baby bok choy stir-fried with garlic and a light seasoning, delivering a fresh, slightly crunchy texture with a mild, earthy flavor. A healthy and delicious vegetable side dish that pairs well with any meal."},
        {"name": "Sweet Red Bean Soup", "price": 9.99, "description": "A warm and comforting dessert soup made from slow-cooked red adzuki beans, sweetened to perfection."}
    ]

    daily_special = random.choice(daily_specials)

    context = {
        "daily_special": daily_special,
        "current_time": time.ctime(),
    }

    return render(request, template_name, context)


def confirmation(request):
    """ 
        Process the form submission, and generate a result 
    """
    template_name = "restaurant/confirmation.html"
    
    # Only process if the request method is POST
    if request.method == 'POST':
        # Read the form data into python variables
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        special_instructions = request.POST.get('special_instructions', '')

        # Retrieve ordered menu items
        ordered_items = request.POST.getlist('menu_item')
        
        # Define the menu items and their prices
        menu_items = {
            "Tomato Egg Stir Fry": 14.99,
            "Stir Fry Baby Bok Choy": 12.99,
            "Mala Tang": 18.99,
            "Sweet Red Bean Soup": 8.99,
            # Ensure you also add the daily special's name and price to this dictionary.
        }
        
        # If a daily special was ordered, add it to the total price
        daily_special_name = request.POST.get('daily_special_name', '')
        daily_special_price = request.POST.get('daily_special_price', '')

        if daily_special_name:
            menu_items[daily_special_name] = float(daily_special_price)

        # Calculate the total price
        total_price = 0
        ordered_item_details = []
        
        for item in ordered_items:
            if item in menu_items:
                total_price += menu_items[item]
                ordered_item_details.append({"name": item, "price": menu_items[item]})

        # Calculate the ready time (30-60 minutes from now)
        current_time = datetime.datetime.now()
        random_minutes_add = random.randint(30, 60)
        ready_time = current_time + datetime.timedelta(minutes=random_minutes_add)

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'ordered_items': ordered_item_details,
            'special_instructions': special_instructions,
            'total_price': f"${total_price:.2f}",
            "ready_time": ready_time.strftime("%I:%M %p"),
            "current_time": time.ctime(),
        }
        
        return render(request, template_name, context)
    
    # If the request method is not POST, redirect back to the order form
    return redirect('order')