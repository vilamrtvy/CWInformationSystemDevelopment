# Сторонние пакеты
from flask import Blueprint, render_template, session, request, current_app, redirect

# Модули проекта
from access import login_permission_required
from DB.sql_provider import SQLProvider
from DB.database import work_with_db
from bl_authorization.auth_scenario_factory import auth_dc
from bl_authorization.auth_scenario_factory import auth_mrg
from bl_authorization.auth_scenario_factory import auth_scr


auth = Blueprint('auth', __name__, template_folder='templates')
provider = SQLProvider('sql/auth/')


# Функция авторизации
@auth.route('/', methods=['GET', 'POST'])
@login_permission_required
def login_page():
    title = [None, None]

    if request.method == 'GET':

        # Проверка на прежнюю аутентификацию
        if session.get('id_of_doctor') is not None:

            # Пользователь уже вошел в систему
            print('ОШИБКА 1')
            return render_template('auth_error.html',
                                   name=session.get('name_of_doctor'))

        else:
            title[0] = 'АВТОРИЗАЦИЯ'

            # Страница авторизации для неавторизованного пользователя
            return render_template('login.html',
                                   title=title,
                                   length=1,
                                   name_of_button='Отправить')

    else:
        # Проверка введенных данных
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        # Запрос на нахождение пользователя в БД
        sql = provider.get('authorization.sql',
                           login=username,
                           password=password)

        result = work_with_db(current_app.config['db_config'], sql)

        # Пользователь найден
        if len(result) != 0:
            key = result[0]['post']

            session['access_rights'] = key
            session['id_of_doctor'] = result[0]['doc_id']
            session['name_of_doctor'] = result[0]['doc_name']

            # Пол врача
            session['gender'] = result[0]['gender']

            # Отделение
            session['depart_key_of_doctor'] = result[0]['depart_key']
            session['depart_name_of_doctor'] = result[0]['bran_name']

            auth_scenario_factory = {
                'dc': auth_dc,
                'mrg': auth_mrg,
                'scr': auth_scr
            }

            scenario = auth_scenario_factory.get(key)

            # Успешный вход
            print('УСПЕШНАЯ АВТОРИЗАЦИЯ')
            return scenario()

        # Пользователь не найден
        else:
            title[0] = 'Неверный логин'
            title[1] = 'или пароль'
            print('ОШИБКА 2')

            # Страница авторизации
            return render_template('login.html',
                                   title=title,
                                   length=2,
                                   name_of_button='Повторная авторизация')


# Функция реинициализации
@auth.route('/reauth')
@login_permission_required
def re_authentication():
    # Очистить сессию
    session.clear()
    # Страница авторизации для неавторизованного пользователя
    return redirect('/auth/')
