# Сторонние пакеты
from flask import Blueprint, render_template, current_app, request, session

# Модули проекта
from DB.sql_provider import SQLProvider
from DB.database import work_with_db
from access import login_permission_required
from bl_reporting.title import function_title


reporting = Blueprint('requests', __name__, template_folder='templates')
provider = SQLProvider('sql/profile/')


# Страница с выбором запроса
@reporting.route('/')
@login_permission_required
def profile_menu():

    post = session.get('access_rights')

    if post == 'scr':
        return render_template('menu_scr.html')

    elif post == 'mrga':
        return render_template('menu_assist.html')

    elif post == 'mrg':
        bran_name = session.get('depart_name_of_doctor')
        title_bran = function_title(bran_name)

        context = {
            'title1': 'Сведения о пациентах ' + title_bran,
            'title2': 'Средний возраст пациентов ' + title_bran,
        }

        return render_template('menu_mrg.html', **context)

    else:
        title1 = 'Доступ запрещен'
        title2 = 'Сменить авторизацию'

        return render_template('access_is_denied.html', title1=title1, title2=title2)


# Первый запрос
@reporting.route('/sql1', methods=['GET', 'POST'])
@login_permission_required
def profile_sql1():
    if request.method == 'GET':
        return render_template('input_bran.html')

    else:

        title = [None, None]

        bran_name = request.form.get("department")

        sql = provider.get('profile_sql1.sql', bran_name=bran_name)
        result = work_with_db(current_app.config['db_config'], sql)

        title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ'
        title[1] = function_title(bran_name)

        if not result:
            result = 'Пациенты не найдены'

            context = {
                'title': title,
                'length': 2,
                'result': result
            }

            return render_template("result_with_one_line.html", **context)

        else:
            res_keys = result[0].keys()

            for i in range(0, len(result)):
                if result[i]['dis_date'] is None:
                    result[i]['dis_date'] = ''

            keylist = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ',
                       'ДАТА ВЫПИСКИ', 'ИМЯ ЛЕЧАЩЕГО ВРАЧА']
            context = {
                'title': title,
                'length': 2,
                'list': result,
                'res_keys': res_keys,
                'keylist': keylist
            }

            return render_template("result.html", **context)


# Второй запрос
@reporting.route('/sql2', methods=['GET', 'POST'])
@login_permission_required
def profile_sql2():
    if request.method == 'GET':
        return render_template('input_bran.html')

    else:

        title = [None, None]

        bran_name = request.form.get("department")

        sql = provider.get('profile_sql2.sql', bran_name=bran_name)
        result = work_with_db(current_app.config['db_config'], sql)

        title[0] = 'СРЕДНИЙ ВОЗРАСТ ПАЦИЕНТОВ'
        title[1] = function_title(bran_name)

        if result[0]['age'] is None:
            result = 'Пациенты не найдены'

        else:
            res = result[0]['age']
            age = res % 10

            year = 'лет'
            if age == 1:
                year = 'год'
            if age > 1 and age < 5:
                year = 'года'

            result = str(res) + ' ' + year

        context = {
            'title': title,
            'length': 2,
            'result': result
        }

        return render_template("result_with_one_line.html", **context)


# Третий запрос
@reporting.route('/sql3', methods=['GET', 'POST'])
@login_permission_required
def profile_sql3():
    if request.method == 'GET':
        title = 'ВРАЧИ, ПРИНЯТЫЕ НА РАБОТУ В ...'
        prompt = 'ВВЕДИТЕ ГОД'

        return render_template('input_days.html', title=title, prompt=prompt)

    else:

        title = [None, None]

        year = request.form.get("days", None)

        sql = provider.get('profile_sql3.sql', year=year)
        result = work_with_db(current_app.config['db_config'], sql)

        title[0] = 'СВЕДЕНИЯ О ВРАЧАХ, ПРИНЯТЫХ'
        title[1] = ' НА РАБОТУ В ' + year + ' ГОДУ'

        if not result:
            result = 'Врачи не найдены'

            context = {
                'title': title,
                'length': 2,
                'result': result
            }

            return render_template("result_with_one_line.html", **context)

        else:
            res_keys = result[0].keys()

            for i in range(0, len(result)):
                if result[i]['doc_dism'] is None:
                    result[i]['doc_dism'] = ''

            keylist = ['ФИО', 'ДАТА ТРУДОУСТРОЙСТВА', 'ДАТА УВОЛЬНЕНИЯ', 'ОТДЕЛЕНИЕ']
            context = {
                'title': title,
                'length': 2,
                'list': result,
                'res_keys': res_keys,
                'keylist': keylist
            }
            return render_template("result.html", **context)


# Четвертый запрос
@reporting.route('/sql4', methods=['GET', 'POST'])
@login_permission_required
def profile_sql4():
    if request.method == 'GET':
        title = 'ПАЦИЕНТЫ, ВЫПИСАВШИЕСЯ ЗА ПОСЛЕДНИЕ ...'
        prompt = 'ВВЕДИТЕ КОЛИЧЕСТВО ДНЕЙ'

        return render_template('input_days.html', title=title, prompt=prompt)

    else:

        title = [None, None, None]
        days = request.form.get("days", None)

        sql = provider.get('profile_sql4.sql', days=days)
        result = work_with_db(current_app.config['db_config'], sql)

        if days == 1:
            title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ,'
            title[1] = 'ВЫПИСАВШИХСЯ'
            title[2] = 'ЗА ПОСЛЕДНИЙ ДЕНЬ'

        else:
            day = 'дней'

            if (int(days) % 10) > 1 and (int(days) % 10) < 5 and (int(days) < 10 or int(days) > 15):
                day = 'дня'

            title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ,'
            title[1] = 'ВЫПИСАВШИХСЯ'
            title[2] = 'ЗА ПОСЛЕДНИЕ ' + days + ' ' + day

        if not result:
            result = 'Пациенты не найдены'

            context = {
                'title': title,
                'length': 3,
                'result': result
            }

            return render_template("result_with_one_line.html", **context)

        else:
            res_keys = result[0].keys()

            keylist = ['ФИО', 'ПАСПОРТ', 'ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ', 'ДАТА ВЫПИСКИ', 'ЛЕЧАЩИЙ ВРАЧ', 'ОТДЕЛЕНИЕ']
            context = {
                'title': title,
                'length': 3,
                'list': result,
                'res_keys': res_keys,
                'keylist': keylist
            }
            return render_template("result.html", **context)


# Пятый запрос
@reporting.route('/sql5', methods=['GET'])
@login_permission_required
def profile_sql5():

    title = [None, None]

    title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ,'
    title[1] = 'НАХОДЯЩИХСЯ В ГОСПИТАЛЕ'
    title[2] = 'НА ДАННЫЙ МОМЕНТ'

    sql = provider.get('profile_sql5.sql')
    result = work_with_db(current_app.config['db_config'], sql)

    res_keys = result[0].keys()

    if not result:
        result = 'Пациенты не найдены'

        context = {
            'title': title,
            'length': 3,
            'result': result
        }

        return render_template("result_with_one_line.html", **context)

    else:

        keylist = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ', 'ЛЕЧАЩИЙ ВРАЧ']
        context = {
            'title': title,
            'length': 2,
            'list': result,
            'res_keys': res_keys,
            'keylist': keylist
        }
        return render_template("result.html", **context)


# Первый запрос для mrg
@reporting.route('/mrg_sql1')
@login_permission_required
def profile_mrg_sql1():

    title = [None, None]
    bran_name = session.get('depart_name_of_doctor')

    sql = provider.get('profile_sql1.sql', bran_name=bran_name)
    result = work_with_db(current_app.config['db_config'], sql)

    title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ'
    title[1] = function_title(bran_name)

    if not result:
        result = 'Пациенты не найдены'

        context = {
            'title': title,
            'length': 2,
            'result': result
        }

        return render_template("result_with_one_line.html", **context)

    else:
        res_keys = result[0].keys()

        for i in range(0, len(result)):
            if result[i]['dis_date'] is None:
                result[i]['dis_date'] = ''

        keylist = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ',
                   'ДАТА ВЫПИСКИ', 'ИМЯ ЛЕЧАЩЕГО ВРАЧА']
        context = {
            'title': title,
            'length': 2,
            'list': result,
            'res_keys': res_keys,
            'keylist': keylist
        }

        return render_template("result.html", **context)


# Второй запрос для mrg
@reporting.route('/mrg_sql2')
@login_permission_required
def profile_mrg_sql2():

    title = [None, None]

    bran_name = session.get('depart_name_of_doctor')

    sql = provider.get('profile_sql2.sql', bran_name=bran_name)
    result = work_with_db(current_app.config['db_config'], sql)

    title[0] = 'СРЕДНИЙ ВОЗРАСТ ПАЦИЕНТОВ'
    title[1] = function_title(bran_name)

    if result[0]['age'] is None:
        result = 'Пациенты не найдены'

    else:
        res = result[0]['age']
        age = res % 10
        year = 'лет'
        if age == 1:
            year = 'год'
        if age > 1 and age < 5:
            year = 'года'

        result = str(res) + ' ' + year

    context = {
        'title': title,
        'length': 2,
        'result': result
    }

    return render_template("result_with_one_line.html", **context)


# Третий запрос для mrg
@reporting.route('/mrg_sql3', methods=['GET', 'POST'])
@login_permission_required
def profile_mrg_sql3():

    if request.method == 'GET':
        title = 'ПАЦИЕНТЫ, ВЫПИСАВШИЕСЯ ЗА ПОСЛЕДНИЕ ...'
        prompt = 'ВВЕДИТЕ КОЛИЧЕСТВО ДНЕЙ'

        return render_template('input_days.html', title=title, prompt=prompt)

    else:
        days = request.form.get("days", None)
        id_of_doctor = session.get('id_of_doctor')

        sql = provider.get('profile_mrg_sql3.sql', days=days, id=id_of_doctor)
        result = work_with_db(current_app.config['db_config'], sql)

        title = [None, None, None]

        if days == 1:
            title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ,'
            title[1] = 'ВЫПИСАВШИХСЯ'
            title[2] = 'ЗА ПОСЛЕДНИЙ ДЕНЬ'

        else:
            day = 'дней'

            if (int(days) % 10) > 1 and (int(days) % 10) < 5 and (int(days) < 10 or int(days) > 15):
                day = 'дня'

            title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ,'
            title[1] = 'ВЫПИСАВШИХСЯ'
            title[2] = 'ЗА ПОСЛЕДНИЕ ' + days + ' ' + day

        if not result:
            result = 'Пациенты не найдены'

            context = {
                'title': title,
                'length': 3,
                'result': result
            }

            return render_template("result_with_one_line.html", **context)

        else:
            res_keys = result[0].keys()

            keylist = ['ФИО', 'ПАСПОРТ', 'ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ', 'ДАТА ВЫПИСКИ', 'ЛЕЧАЩИЙ ВРАЧ', 'ОТДЕЛЕНИЕ']
            context = {
                'title': title,
                'length': 3,
                'list': result,
                'res_keys': res_keys,
                'keylist': keylist
            }
            return render_template("result.html", **context)


# Четвертый запрос для mrg
@reporting.route('/mrg_sql4', methods=['GET'])
@login_permission_required
def profile_mrg_sql4():

    dep_key = session.get('depart_key_of_doctor')

    sql = provider.get('profile_mrg_sql4.sql', id=dep_key)
    result = work_with_db(current_app.config['db_config'], sql)

    if not result:
        result = 'Пациенты не найдены'

        title = [None, None, None]

        title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ,'
        title[1] = 'НАХОДЯЩИХСЯ В ВАШЕМ ОТДЕЛЕНИИ'
        title[2] = 'НА ДАННЫЙ МОМЕНТ'

        context = {
            'title': title,
            'length': 3,
            'result': result
        }

        return render_template("result_with_one_line.html", **context)

    else:
        res_keys = result[0].keys()

        title = [None]

        title[0] = 'СВЕДЕНИЯ О ПАЦИЕНТАХ'

        keylist = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ', 'ЛЕЧАЩИЙ ВРАЧ']
        context = {
            'title': title,
            'length': 1,
            'list': result,
            'res_keys': res_keys,
            'keylist': keylist
        }
        return render_template("result.html", **context)
