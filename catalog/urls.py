from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('blog/', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blog_post_create'),
    path('blog/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('blog/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),
]
