from django.urls import path
from . import views
from .views import *
from users.views import RegisterView
from django.views.decorators.cache import cache_page
from .views import (
    RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    MailingSettingsCreateView, MailingSettingsUpdateView, MailingSettingsDeleteView,
    MessageCreateView, MessageUpdateView, MessageDeleteView
)

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    # r'i gj pflfyb.
    path('product/<int:pk>/', cache_page(60 * 15)(views.ProductDetailView.as_view()), name='product_detail'),
    path('blog/', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blog_post_create'),
    path('blog/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('blog/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),

    # Курсовая
    path('model/actions/', views.model_actions, name='model_actions'),

    path('recipient/list/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('mailingsettings/create/', MailingSettingsCreateView.as_view(), name='mailingsettings_create'),
    path('mailingsettings/<int:pk>/update/', MailingSettingsUpdateView.as_view(), name='mailingsettings_update'),
    path('mailingsettings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='mailingsettings_delete'),
    path('mailingsettings/list/', MailingSettingsListView.as_view(), name='mailingsettings_list'),

    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', message_detail, name='message_detail'),

    # Задачи от 14го
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('version/', version_form, name='version_form'),
    path('users/register/', RegisterView.as_view(), name='register'),

    path('categories/', CategoryListView.as_view(), name='category_list'),

]
