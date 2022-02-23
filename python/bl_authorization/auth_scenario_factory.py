# Сторонние пакеты
from flask import render_template, session, current_app

# Модули проекта
from DB.sql_provider import SQLProvider
from DB.database import work_with_db
from bl_authorization.title1 import post_function

provider_notices = SQLProvider('sql/notice')


# Пользователь - доктор
def auth_dc():
    gender = session.get('gender')

    # Должность врача и фотография
    func_res = post_function(session.get('depart_key_of_doctor'),
                             gender,
                             session.get('access_rights'))

    position = func_res[0]
    image = func_res[1]

    length = len(position)

    # Имя врача
    name = session.get('name_of_doctor')

    sql = provider_notices.get('notices_of_doctor.sql',
                               id=session.get('id_of_doctor'))

    result = work_with_db(current_app.config['db_config'], sql)
    notices = len(result)

    if notices != 0:
        session['notices'] = notices
        context = {
            'name': name,
            'position': position,
            'length': int(length),
            'image': image,
            'amount': notices
        }
    else:
        context = {
            'name': name,
            'position': position,
            'length': int(length),
            'image': image
        }

    session.pop('gender')
    return render_template('successfully_dc.html', **context)


# Пользователь - заведующая/ий отделением
def auth_mrg():
    gender = session.get('gender')

    # Должность врача и фотография
    func_res = post_function(session.get('depart_key_of_doctor'),
                             gender,
                             session.get('access_rights'))

    position = func_res[0]
    image = func_res[1]

    length = len(position)

    # Имя врача
    name = session.get('name_of_doctor')

    sql = provider_notices.get('notices_of_doctor.sql',
                               id=session.get('id_of_doctor'))

    result = work_with_db(current_app.config['db_config'], sql)
    notices = len(result)

    if notices != 0:
        session['notices'] = notices
        context = {
            'name': name,
            'position': position,
            'length': int(length),
            'image': image,
            'amount': notices
        }
    else:
        context = {
            'name': name,
            'position': position,
            'length': int(length),
            'image': image
        }

    session.pop('gender')
    return render_template('successfully_mrg.html', **context)


# Пользователь - секретарь
def auth_scr():
    gender = session.get('gender')

    # Должность врача и фотография
    func_res = post_function(session.get('depart_key_of_doctor'),
                             gender,
                             session.get('access_rights'))

    position = func_res[0]
    image = func_res[1]

    # Имя врача
    name = session.get('name_of_doctor')

    context = {
        'name': name,
        'position': position,
        'length': 1,
        'image': image
    }

    session.pop('gender')
    return render_template('successfully_scr.html', **context)
