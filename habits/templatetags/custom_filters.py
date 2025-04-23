from django import template

register = template.Library()

@register.filter
def replace_commas_with_dot(value):
    """
    カンマを「・」に変換するテンプレートフィルター
    """
    if isinstance(value, str):
        return value.replace(",", "・")
    return value
