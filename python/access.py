# Сторонние пакеты
from flask import session, request, current_app, render_template
from functools import wraps


def group_permission_validation():
    config = current_app.config['ACCESS_CONFIG']
    group_name = session.get('access_rights', 'unauthorized')
    t = request.endpoint.split('.')
    target_app = t[len(t) - 1]

    if group_name in config and target_app in config[group_name]:
        return True
    return False


def login_permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return f(*args, **kwargs)
        if session.get('access_rights') is not None:
            title1 = 'Доступ запрещен'
            title2 = 'Сменить авторизацию'
        else:
            title1 = 'Вы не авторизованы'
            title2 = 'Авторизоваться'
        return render_template('access_is_denied.html',
                               title1=title1,
                               title2=title2)
    return wrapper
