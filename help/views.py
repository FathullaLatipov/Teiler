from django.shortcuts import render
from django.views.generic import ListView

from help.models import HelpModel


class HelpListView(ListView):
    template_name = 'articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return HelpModel.objects.order_by('pk')
