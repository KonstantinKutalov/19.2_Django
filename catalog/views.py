from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView, \
    UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import BlogPost, Product, Recipient, MailingSettings, Message
from .forms import RecipientForm, MailingSettingsForm, MessageForm



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
