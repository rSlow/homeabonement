from django import template

register = template.Library()


@register.filter
def name_or_username(value):
    if hasattr(value, "first_name") and value.first_name:
        return value.first_name
    elif hasattr(value, "email") and value.email:
        return value.email
    elif hasattr(value, "username") and value.username:
        return value.username
    else:
        raise AttributeError(f"Object {value} haven't first name, username or email. Is value a User object?")
