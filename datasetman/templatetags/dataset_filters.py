from django import template

from core import models

register = template.Library()


def parse_raven_dataset_id(value):
    """Remueve la parte del ID del dataset que define raven db"""
    return value.replace('datasets/', '')


def get_dict_value(value, arg):
    """Saca el valor de un dictionario dada una llave"""
    return value[arg]


def uploaded_by_name_user(value):
    user = models.User.objects.get(pk=value)

    name = ""

    if user.first_name and user.last_name:
        name = f"{user.first_name} {user.last_name}"

    return name


def uploaded_by_user(value):
    user = models.User.objects.get(pk=value)
    return user.username


def user_profile_pic(value):
    user = models.User.objects.get(pk=value)
    return user.photo


register.filter('parse_raven_dataset_id', parse_raven_dataset_id)
register.filter('get_dict_value', get_dict_value)
register.filter('uploaded_by_name_user', uploaded_by_name_user)
register.filter('uploaded_by_user', uploaded_by_user)
register.filter('user_profile_pic', user_profile_pic)
