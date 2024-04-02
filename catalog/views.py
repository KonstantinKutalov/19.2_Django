from django.views.generic import TemplateView, DeleteView, CreateView, \
    UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import BlogPost, Product, Recipient, MailingSettings, Message, Version
from .forms import RecipientForm, MailingSettingsForm, MessageForm, ProductForm, VersionFormStyled
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

from django.views.generic import ListView
from catalog.services import get_cached_categories

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_version = Version.get_active_version_for_product(product)
        is_active_version = active_version.is_active if active_version else False
        context['is_active_version'] = is_active_version
        return context


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog_posts'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog_post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'published']

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'published']

    def get_success_url(self):
        return reverse_lazy('blog_post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog_post_list')
    template_name = 'blog/blogpost_confirm_delete.html'
    context_object_name = 'blog_post'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipient_list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipient_list')


class RecipientListView(ListView):
    model = Recipient


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailingsettings_list')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailingsettings_list')


class MailingSettingsListView(ListView):
    model = MailingSettings


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


# Задачи от 14го


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        active_versions = {}
        for product in products:
            active_version = Version.get_active_version_for_product(product)
            is_active_version = active_version.is_active if active_version else False
            active_versions[product.pk] = is_active_version
        context['active_versions'] = active_versions
        return context


class ProductCreateView(LoginRequiredMixin, AccessMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # Привязка текущего пользователя к создаваемому продукту
        form.instance.owner = self.request.user
        return super().form_valid(form)

    login_message = "Зарегистрируйтесь, чтобы добавить товар"
    redirect_field_name = 'next'

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.info(self.request, self.login_message)
        return redirect(reverse_lazy('register') + '?next=' + self.request.path)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    # Проверка на суперпользователя или модератора
    @user_passes_test(lambda u: u.is_superuser or u.is_staff)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        instance = self.get_object()
        if user.is_staff:  # Если пользователь является модератором
            fields_to_disable = ['name', 'price', 'created_at',
                                 'updated_at']  # Поля, которые нужно отключить для модератора
            for field in fields_to_disable:
                form.fields[field].disabled = True
        return form


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, является ли текущий пользователь владельцем продукта
        product = self.get_object()
        if product.owner != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def version_form(request):
    if request.method == 'POST':
        form = VersionFormStyled(request.POST)
        if form.is_valid():
            # Обработка валидной формы
            form.save()
            return HttpResponse('Form submitted successfully!')
    else:
        form = VersionFormStyled()
    return render(request, 'version_form.html', {'form': form})


class RegisterView(TemplateView):
    template_name = 'users/register.html'



class CategoryListView(ListView):
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_cached_categories()