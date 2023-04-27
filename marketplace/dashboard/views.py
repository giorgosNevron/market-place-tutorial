from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from items.models import Item

class ItemsDashboard(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/dashboard_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.filter(created_by=self.request.user)
        context['items'] = items 

        return context
