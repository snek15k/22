from django.urls import path
from .views import (
    HomeView, ContactsView, ProductDetailView,
    ProductListView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, ProductUnpublishView
)

urlpatterns = [
    # Главная страница
    path('', HomeView.as_view(), name='home'),

    # Контакты
    path('contacts/', ContactsView.as_view(), name='contacts'),

    # Детали товара
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # CRUD: список, создание, редактирование, удаление
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
]
