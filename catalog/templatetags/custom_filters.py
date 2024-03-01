from django import template

register = template.Library()


@register.filter
def add_media_prefix(value):
    if value:
        return f'/media/{value}'
    return '#'  # Если значение пустое, возвращаем #
