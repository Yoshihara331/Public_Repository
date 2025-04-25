from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={**field.field.widget.attrs, 'class': css_class})

@register.filter(name='replace_commas_with_dot')
def replace_commas_with_dot(value):
    if isinstance(value, str):
        return value.replace(',', '・')
    return value

@register.filter(name='dict_get')
def dict_get(dict_data, key):
    if dict_data is None:
        return None
    return dict_data.get(key)

@register.filter(name='get_item')
def get_item(dict_data, key):
    if dict_data is None:
        return None
    return dict_data.get(key)
