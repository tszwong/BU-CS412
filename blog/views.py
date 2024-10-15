# blog/views.py
# views to show the blog application
import random
from django.shortcuts import render

from . models import * 
from django.views.generic import ListView, DetailView

# class-based view
class ShowAllView(ListView):
    '''A view to show all Articles.'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class RandomArticleView(DetailView):
    model = Article
    template_nmae = "blog/article.html"
    context_object_name = "article"

    def get_object(self):
        """
            return the instance of the Article object to show
        """

        # get all articles
        all_articles = Article.objects.all()  # SELECT *

        # pick one at random
        return random.choice(all_articles)
    
class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template!!
    context_object_name = 'article'