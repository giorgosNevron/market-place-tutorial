from django.views.generic import TemplateView,ListView,DeleteView,FormView,UpdateView,DetailView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewItemForm, EditItemForm
from .models import Category, Item


class Items(TemplateView):
    template_name = 'items/items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')
        category_id = self.request.GET.get('category', 0)
        categories = Category.objects.all()
        items = Item.objects.filter(is_sold=False)

        if category_id:
            items = items.filter(category_id=category_id)

        if query:
            items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

        context['items'] = items 
        context['query'] = query 
        context['categories'] = categories
        context['category_id'] = int(category_id)

        return context

class ItemDetails(LoginRequiredMixin,DetailView):
    model = Item
    template_name = 'items/items_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item=get_object_or_404(Item, pk=self.kwargs['pk'])
        related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=self.kwargs['pk'])[0:3]
        context['related_items'] = related_items
        return context


class NewItem(LoginRequiredMixin,FormView):
    form_class = NewItemForm
    template_name = 'items/new_item.html'
    success_url = '/'

    def form_valid(self,form):
        form = NewItemForm(self.request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()

            return super().form_valid(form)
        else:
            return super().form_invalid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class EditItem(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'items/items_edit.html'
    form_class = EditItemForm
    success_url = '/'

    def get_object(self):
        website = Item.objects.get(pk=self.kwargs['pk'])
        return website

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = Item.objects.get(pk=self.kwargs['pk'])
        context['website'] = item
        return context


class DeleteItem(LoginRequiredMixin,DeleteView):
    model = Item
    template_name ='items/items_delete.html'
    success_url = '/'

    def get_object(self):
        item = Item.objects.get(pk=self.kwargs['pk'])
        return item
