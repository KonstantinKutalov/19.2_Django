from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

NULLABLE = {'blank': True, 'null': True}


def default_manufactured_at():
    return timezone.now().date()


class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    avatar = models.ImageField(upload_to="students/", verbose_name='аватар', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='учится')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ('last_name',)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    manufactured_at = models.DateField(default=timezone.now, verbose_name='Дата производства продукта')
    attribute1 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Атрибут 1')
    attribute2 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Атрибут 2')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-адрес')
    content = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='blog_previews/', blank=True, null=True, verbose_name='Превью')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'


class Recipient(models.Model):
    email = models.EmailField(_('Email'))
    full_name = models.CharField(_('Full Name'), max_length=100)
    comment = models.TextField(_('Comment'), blank=True)

    def __str__(self):
        return self.email


# От по курсовой
class MailingSettings(models.Model):
    TIME_CHOICES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
    )
    send_time = models.TimeField(_('Send Time'))
    frequency = models.CharField(_('Frequency'), max_length=10, choices=TIME_CHOICES)
    status = models.CharField(_('Status'), max_length=20, default='created')


class Message(models.Model):
    subject = models.CharField(_('Subject'), max_length=255)
    body = models.TextField(_('Body'))


class MailingLog(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    server_response = models.TextField(blank=True)

    def __str__(self):
        return f"{self.recipient.email} - {self.timestamp}"


# До

# Задачи от 14го

class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    version_number = models.CharField(max_length=100)
    version_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.product} - {self.version_number} ({self.version_name})"

    @staticmethod
    def get_active_version_for_product(product):
        try:
            return Version.objects.filter(product=product, is_active=True).latest('created_at')
        except Version.DoesNotExist:
            return None

        # Если необходимо обработать случай более одной активной версии, например, выбрать самую новую версию:
        except Version.MultipleObjectsReturned:
            return Version.objects.filter(product=product, is_active=True).order_by('-created_at').first()
