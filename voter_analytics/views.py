from ast import List
from django import forms
import django
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from voter_analytics.models import Voter
from django.db.models import Count
import plotly.express as px
from plotly.io import to_html

# Create your views here.
class VotersView(ListView):
    """
        interface to provide a listing of Voter records
    """

    model = Voter
    template_name = 'voter_analytics/show_voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()

        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET.get('party_affiliation')
            if party_affiliation:
                qs = qs.filter(party_affiliation=party_affiliation)
        
        if 'min_birth_year' in self.request.GET:
            min_birth_year = self.request.GET.get('min_birth_year')
            if min_birth_year:
                qs = qs.filter(dob__year__gte=min_birth_year)

        if 'max_birth_year' in self.request.GET:
            max_birth_year = self.request.GET.get('max_birth_year')
            if max_birth_year:
                qs = qs.filter(dob__year__lte=max_birth_year)

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET.get('voter_score')
            if voter_score:
                qs = qs.filter(voter_score=voter_score)

        if 'v20state' in self.request.GET:
            if self.request.GET.get('v20state') == '1':
                qs = qs.filter(v20state=True)

        if 'v21town' in self.request.GET:
            if self.request.GET.get('v21town') == '1':
                qs = qs.filter(v21town=True)

        if 'v21primary' in self.request.GET:
            if self.request.GET.get('v21primary') == '1':
                qs = qs.filter(v21primary=True)

        if 'v22general' in self.request.GET:
            if self.request.GET.get('v22general') == '1':
                qs = qs.filter(v22general=True)

        if 'v23town' in self.request.GET:
            if self.request.GET.get('v23town') == '1':
                qs = qs.filter(v23town=True)

        return qs
    

class VoterDetailView(DetailView):
    """
        interface to provide a detailed view of a single Voter record
    """

    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class VoterGraphsView(ListView):
    """
        interface to graphics based on Voter records
    """
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'graphs'

    def get_queryset(self):
        return Voter.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Distribution of Voters by Year of Birth (Histogram)
        birth_year_data = Voter.objects.values('dob__year').annotate(count=Count('dob__year'))
        birth_years = [entry['dob__year'] for entry in birth_year_data]
        birth_counts = [entry['count'] for entry in birth_year_data]
        birth_year_chart = px.bar(
            x=birth_years,
            y=birth_counts,
            title='Distribution of Voters by Year of Birth',
            labels={'x': 'Year of Birth', 'y': 'Number of Voters'}
        )
        context['birth_year_chart'] = to_html(birth_year_chart, full_html=False)

        # 2. Distribution of Voters by Party Affiliation (Pie Chart)
        party_data = Voter.objects.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_labels = [entry['party_affiliation'] for entry in party_data]
        party_counts = [entry['count'] for entry in party_data]
        party_chart = px.pie(
            names=party_labels,
            values=party_counts,
            title='Party Affiliation Distribution'
        )
        context['party_chart'] = to_html(party_chart, full_html=False)

        # 3. Distribution of Voter Participation in Each Election (Bar Chart)
        elections = {
            '2020 State Election': Voter.objects.filter(v20state=True).count(),
            '2021 Town Election': Voter.objects.filter(v21town=True).count(),
            '2021 Primary Election': Voter.objects.filter(v21primary=True).count(),
            '2022 General Election': Voter.objects.filter(v22general=True).count(),
            '2023 Town Election': Voter.objects.filter(v23town=True).count(),
        }
        election_chart = px.bar(
            x=list(elections.keys()),
            y=list(elections.values()),
            title='Voter Participation in Elections',
            labels={'x': 'Election', 'y': 'Number of Voters'}
        )
        context['election_chart'] = to_html(election_chart, full_html=False)

        return context
