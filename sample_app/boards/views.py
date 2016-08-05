from django.shortcuts import render

# Create your views here.
from toolkit.views import CCEListView, CCETemplateView


class BoardListView(CCETemplateView):
    template_name = 'base.html'
    page_title = 'TEST'
    sidebar_group = ['home']
