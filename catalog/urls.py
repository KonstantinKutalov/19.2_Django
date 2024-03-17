from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('blog/', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blog_post_create'),
    path('blog/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('blog/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),

    # Подготовка к курсовой
    path('recipient/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/', RecipientListView.as_view(), name='recipient_list'),
    path('mailingsettings/', MailingSettingsCreateView.as_view(), name='mailingsettings_create'),
    path('mailingsettings/<int:pk>/update/', MailingSettingsUpdateView.as_view(), name='mailingsettings_update'),
    path('mailingsettings/', MailingSettingsListView.as_view(), name='mailingsettings_list'),
    path('message/', MessageCreateView.as_view(), name='message_create'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),

    # Задачи от 14го
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('version/', version_form, name='version_form'),

]

