from django.views.generic import ListView, DetailView, TemplateView, View
from django.shortcuts import render
from .models import Product
from blog.models import BlogPost


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['latest_posts'] = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request):
        return render(request, self.template_name, {'success': False})

    def post(self, request):
        message = request.POST.get('message')
        return render(request, self.template_name, {'success': True})
