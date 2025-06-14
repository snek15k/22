from django.views.generic import (
    ListView, DetailView, TemplateView, View,
    CreateView, UpdateView, DeleteView
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product
from .forms import ProductForm
from blog.models import BlogPost

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .services import get_products_by_category
from .models import Product

from django.core.cache import cache


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['latest_posts'] = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
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


# CRUD for Product

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        cache_key = f'products_in_category_{form.instance.category_id}'
        cache.delete(cache_key)
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        cache_key = f'products_in_category_{form.instance.category_id}'
        cache.delete(cache_key)
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        is_owner = obj.owner == user
        is_moderator = user.has_perm('catalog.delete_product')
        if not (is_owner or is_moderator):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        cache_key = f'products_in_category_{self.object.category_id}'
        cache.delete(cache_key)
        return super().delete(request, *args, **kwargs)


class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    raise_exception = True

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.status = Product.STATUS_DRAFT
        product.save()
        cache_key = f'products_in_category_{product.category_id}'
        cache.delete(cache_key)
        messages.success(request, f'Продукт "{product.name}" снят с публикации.')
        return redirect(reverse_lazy('product_detail', kwargs={'pk': pk}))


class CategoryProductListView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        return context
