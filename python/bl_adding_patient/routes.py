# Стандартные пакеты
from datetime import datetime

# Сторонние пакеты
from flask import Blueprint, render_template, session, request, current_app, redirect
import numpy

# Модули проекта
from access import login_permission_required
from DB.sql_provider import SQLProvider
from DB.database import work_with_db, make_update
from bl_adding_patient.diseases import all_diseases
from bl_adding_patient.scenario_stage import searching_stage_of_user


add_patient = Blueprint('patient', __name__, template_folder='templates')
provider = SQLProvider('sql/patient/')


# Функция проверки
@add_patient.route('/')
@login_permission_required
def check():

    stage = session.get('stage')

    stage_of_user = searching_stage_of_user(stage)

    return redirect(stage_of_user)

# Функция выбора варианта добавления пациента
@add_patient.route('/main_menu')
@login_permission_required
def add_or_found_patient():

    session['stage'] = None

    return render_template('step1_add_or_found.html')


# Функция добавления основной информации
@add_patient.route('/add', methods=['GET', 'POST'])
@login_permission_required
def add_patient_info():

    session['search'] = 0
    session['stage'] = None

    # Страница добавления пациента
    if request.method == 'GET':

        context = {
            'name': '',
            'birthday': '',
            'passport': '',
            'address': '',
            'url': '/patient/main_menu'
        }

        return render_template('step1_add.html', **context)

    # Занесение информации в сессию
    else:

        session['id_of_patient'] = None

        session['patient_info'] = [request.form.get('patient_name'),
                                   request.form.get('patient_birthday'),
                                   request.form.get('patient_passport'),
                                   request.form.get('patient_address')]

        return redirect('/patient/add_accept')


# Функция добавления основной информации
@add_patient.route('/add_accept', methods=['GET', 'POST'])
@login_permission_required
def add_accept():
    if request.method == 'GET':

        label_list = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'СЕРИЯ И НОМЕР ПАСПОРТА',
                      'АДРЕС ПРОЖИВАНИЯ / РЕГИСТРАЦИИ']
        length = 4

        context = {
            'length': length,
            'label_list': label_list,
            'info_about_patient': session.get('patient_info')
        }

        return render_template('step1_added_patient.html', **context)

    else:

        if session.get('access_rights') == 'scr':
            session['status'] = 1
            return redirect('/patient/brans')

        else:
            if session.get('access_rights') == 'mrg':
                return redirect('/patient/doctors')

            if session.get('access_rights') == 'dc':
                session['status'] = 2
                return redirect('/patient/diseases')


# Функция поиска пациента
@add_patient.route('/found', methods=['GET', 'POST'])
@login_permission_required
def found_patient():

    session['search'] = 1
    session['stage'] = None

    if request.method == 'GET':
        return render_template('step1_found.html')

    else:
        surname = request.form.get('patient_surname')
        name = request.form.get('patient_name')

        if surname is not None or name is not None:
            # Пациенты найдены
            session['entered_surname'] = surname
            session['entered_name'] = name

        return redirect('/patient/founded_patients')


# Функция выбора пациента
@add_patient.route('/founded_patients', methods=['GET', 'POST'])
@login_permission_required
def founded_patients():

    session['stage'] = 2

    sql = provider.get('find_patient.sql',
                       surname=session.get('entered_surname'),
                       name=session.get('entered_name'))

    list_of_patients = work_with_db(current_app.config['db_config'], sql)

    j = 0

    for i in range(0, len(list_of_patients)):

        if list_of_patients[j]['sum_index'] == 1:
            list_of_patients = numpy.delete(list_of_patients, j, axis=0)
        else:
            j += 1

    if request.method == 'GET':

        # Пациенты найдены
        if len(list_of_patients) != 0:
            length = len(list_of_patients)

            context = {
                'length': length,
                'pat_id': 'pat_id',
                'pat_name': 'pat_name',
                'list_of_patients': list_of_patients
            }

            return render_template('step1_founded_patients.html', **context)

        else:
            session.pop('stage')
            return render_template('step1_not_founded.html')

    else:
        session['id_of_patient'] = request.form.get("patient")

        return redirect('/patient/founded_patient')


# Информация о выбранном пациенте из базы данных
@add_patient.route('/founded_patient', methods=['GET', 'POST'])
@login_permission_required
def founded_patient():

    session['stage'] = 3

    if request.method == 'GET':

        sql = provider.get('info_about_choosed_patient.sql', id=session.get('id_of_patient'))
        info_about_patient = work_with_db(current_app.config['db_config'], sql)

        info_list = ['pat_name', 'pat_birthday', 'pat_passport', 'pat_address']

        label_list = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'СЕРИЯ И НОМЕР ПАСПОРТА',
                      'АДРЕС ПРОЖИВАНИЯ / РЕГИСТРАЦИИ']
        length = 4

        context = {
            'length': length,
            'label_list': label_list,
            'info_list': info_list,
            'info_about_patient': info_about_patient
        }

        return render_template('step1_founded_patient.html', **context)

    else:

        session.pop('entered_surname')
        session.pop('entered_name')

        if session.get('access_rights') == 'scr':
            session['status'] = 1
            return redirect('/patient/brans')

        else:
            if session.get('access_rights') == 'mrg':
                return redirect('/patient/doctors')

            if session.get('access_rights') == 'dc':
                session['status'] = 2
                return redirect('/patient/diseases')


# Функция выбора отделения
@add_patient.route('/brans', methods=['GET', 'POST'])
@login_permission_required
def choose_brans():

    session['stage'] = 4

    # Страница выбора отделения
    if request.method == 'GET':
        return render_template('step2_choose_bran.html')

    else:
        session['department_of_patient'] = request.form.get('department')

        return redirect('/patient/doctors')


# Функция выбора врача
@add_patient.route('/doctors', methods=['GET', 'POST'])
@login_permission_required
def choose_doctors():

    session['stage'] = 5

    # Страница выбора отделения
    if request.method == 'GET':
        if session.get('department_of_patient') is None:
            session['department_of_patient'] = session.get('depart_name_of_doctor')

        sql = provider.get('get_doctors.sql',
                           depart_name=session.get('department_of_patient'))
        doctors = work_with_db(current_app.config['db_config'], sql)

        length = len(doctors)

        context = {
            'list_of_doctors': doctors,
            'doc_id': 'doc_id',
            'doc_name': 'doc_name',
            'length': int(length)
        }

        return render_template('step3_choose_doctor.html', **context)

    else:
        doctor_of_patient = request.form.get('doctor')

        if session.get('access_rights') == 'scr':
            session['doctor_of_patient'] = doctor_of_patient
            return redirect('/patient/info')

        if session.get('access_rights') == 'mrg':
            if int(doctor_of_patient) == int(session.get('id_of_doctor')):
                session.pop('department_of_patient')
                session['status'] = 2
                return redirect('/patient/diseases')
            else:
                session['doctor_of_patient'] = doctor_of_patient
                session['status'] = 1
                return redirect('/patient/info')


# Функция выбора заболевания
@add_patient.route('/diseases', methods=['GET', 'POST'])
@login_permission_required
def choose_disease():

    session['stage'] = 6

    # Страница выбора заболевания
    if request.method == 'GET':
        # Заболевания для конкретного отделения больницы

        diseases = all_diseases(session.get('depart_key_of_doctor'))

        length = len(diseases) / 3

        if int(session.get('status')) == 3:
            if int(session.get('search')) == 0:
                url = '/patient/add'
            elif int(session.get('search')) == 1:
                url = '/patient/founded_patient'

        if int(session.get('status')) == 2:
            url = '/patient/doctors'

        context = {
            'length': int(length),
            'list_of_diseases': diseases,
            'url': url
        }

        return render_template('step4_choose_disease.html', **context)

    # Занесение диагноза в сессию
    else:
        # Диагноз
        disease = request.form.get("disease")
        session['disease_of_patient'] = disease

        return redirect('/patient/ward')


# Функция выбора палаты
@add_patient.route('/ward', methods=['GET', 'POST'])
@login_permission_required
def choose_ward():

    session['stage'] = 7

    if request.method == 'GET':

        dep_key = session.get('depart_key_of_doctor')

        sql = provider.get('find_wards.sql', dep_key=dep_key)
        wards = work_with_db(current_app.config['db_config'], sql)
        print(wards)

        sql = provider.get('busy_wards.sql', dep_key=dep_key)
        busy = work_with_db(current_app.config['db_config'], sql)
        print(busy)

        for i in range(0, len(wards)):
            for j in range(0, len(busy)):
                if wards[i]['ward_id'] == busy[j]['ward_id']:
                    wards[i]['limited'] = wards[i]['limited'] - busy[j]['amount']
                    print(wards[i]['limited'])

        j = 0
        for i in range(0, len(wards)):
            limit = int(wards[j]['limited'])
            if limit == int(wards[j]['ward_places']):
                wards[j]['limited'] = limit
                wards = numpy.delete(wards, j, axis=0)
            else:
                wards[j]['ward_places'] = int(wards[j]['ward_places']) - limit
                j += 1

        if len(wards) == 0:

            return render_template('step5_error.html')

        else:

            context = {
                'ward_number': 'ward_number',
                'ward_cat': 'ward_cat',
                'ward_places': 'ward_places',
                'ward_id': 'ward_id',
                'wards': wards,
                'url': '/patient/diseases'
            }

            return render_template('step5_choose_ward.html', **context)

    else:
        # Номер палаты
        ward_id = request.form.get("number_ward")
        session['ward_of_patient'] = ward_id

        return redirect('/patient/info')


# Карта пациента
@add_patient.route('/info')
@login_permission_required
def info_card():

    session['stage'] = 8

    status = int(session.get('status'))

    title_list = ['ФИО', 'ДАТА РОЖДЕНИЯ',
                  'НОМЕР ПАСПОРТА', 'АДРЕС ПРОЖИВАНИЯ']

    # Для пациентов в статусе ожидания
    if status == 1:
        session['history'] = [session.get('department_of_patient'),
                              session.get('doctor_of_patient')]

        history_list = ['ДАТА ПОСТУПЛЕНИЯ', 'ОТДЕЛЕНИЕ',
                        'ЛЕЧАЩИЙ ВРАЧ', 'СТАТУС']

        sql = provider.get('history_status_1.sql',
                           doctor_id=session.get('doctor_of_patient'))

        pattern_history = work_with_db(current_app.config['db_config'], sql)

        history = [datetime.today().strftime('%Y-%m-%d'),
                   pattern_history[0]['bran_name'],
                   pattern_history[0]['doc_name'],
                   'ОЖИДАЕТ ПОДТВЕРЖДЕНИЯ']

        length = len(history)

    # Для пациентов на лечении
    else:
        session['history'] = [session.get('disease_of_patient'),
                              session.get('depart_key_of_doctor'),
                              session.get('ward_of_patient'),
                              session.get('id_of_doctor')]

        history_list = ['ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ', 'ОТДЕЛЕНИЕ',
                        'НОМЕР ПАЛАТЫ', 'ЛЕЧАЩИЙ ВРАЧ', 'СТАТУС']

        sql = provider.get('history_status_2.sql',
                           doctor_id=session.get('id_of_doctor'),
                           ward_id=session.get('ward_of_patient'))

        pattern_history = work_with_db(current_app.config['db_config'], sql)

        history = [datetime.today().strftime('%Y-%m-%d'),
                   session.get('disease_of_patient'),
                   pattern_history[0]['bran_name'],
                   pattern_history[0]['ward_number'],
                   pattern_history[0]['doc_name'],
                   'НА ЛЕЧЕНИИ']

        length = len(history)

    patient_status = 'from_db'

    # Для новых пользователей
    if session.get('id_of_patient') is None:
        patient = session.get('patient_info')

        patient_status = 'new_patient'

        if status == 1:
            url = '/patient/edit_bio'
        else:
            url = '/patient/edit_disease_or_ward'

        context = {
            'info_list': patient,
            'title_list': title_list,
            'history_list': history_list,
            'length': length,
            'list': history
        }

    # Для пользователей из базы данных
    else:
        patient_id = int(session.get('id_of_patient'))

        sql = provider.get('found_info.sql', pat_id=patient_id)
        pattern = work_with_db(current_app.config['db_config'], sql)

        patient = [pattern[0]['pat_name'],
                   pattern[0]['pat_passport'],
                   pattern[0]['pat_birthday'],
                   pattern[0]['pat_address']]

        url = '/patient/edit_disease_or_ward'

        context = {
            'info_list': patient,
            'title_list': title_list,
            'history_list': history_list,
            'length': length,
            'list': history
        }

    if patient_status == 'new_patient':
        return render_template('step6_patient_from_db.html',
                               **context,
                               url=url)

    else:
        if status == 2:
            return render_template('step6_patient_from_db.html',
                                   **context,
                                   url=url)
        else:
            return render_template('step6_patient_from_db_wa.html',
                                   **context)


# Окно выбора изменения диагноза или номера палаты
@add_patient.route('/edit_disease_or_ward')
@login_permission_required
def edit_disease_or_ward():

    session['stage'] = 9

    if session.get('id_of_patient') is None:
        return render_template('step7_wanna_edit_wn.html')
    else:
        return render_template('step7_wanna_edit.html')


# Функция изменения диагноза
@add_patient.route('/edit_disease', methods=['GET', 'POST'])
@login_permission_required
def edit_disease():

    session['stage'] = 10

    if request.method == 'GET':

        diseases = all_diseases(session.get('depart_key_of_doctor'))

        length = len(diseases) / 3

        context = {
            'length': int(length),
            'list_of_diseases': diseases,
            'url': '/patient/info'
        }

        return render_template('step4_choose_disease.html', **context)

    else:
        session['disease_of_patient'] = request.form.get('disease')

        return redirect('/patient/info')


# Функция изменения палаты
@add_patient.route('/edit_ward', methods=['GET', 'POST'])
@login_permission_required
def edit_ward():

    session['stage'] = 11

    if request.method == 'GET':

        dep_key = session.get('depart_key_of_doctor')

        sql = provider.get('find_wards.sql', dep_key=dep_key)
        wards = work_with_db(current_app.config['db_config'], sql)

        sql = provider.get('busy_wards.sql', dep_key=dep_key)
        busy = work_with_db(current_app.config['db_config'], sql)

        for i in range(0, len(wards)):
            for j in range(0, len(busy)):
                if wards[i]['ward_id'] == busy[j]['ward_id']:
                    wards[i]['limited'] = wards[i]['limited'] - busy[j]['amount']

        j = 0
        for i in range(0, len(wards)):
            limit = int(wards[j]['limited'])
            if limit == int(wards[j]['ward_places']):
                wards[j]['limited'] = limit
                wards = numpy.delete(wards, j, axis=0)
            else:
                wards[j]['ward_places'] = int(wards[j]['ward_places']) - limit
                j += 1

        if len(wards) == 0:
            return render_template('step5_error.html')

        else:

            context = {
                'ward_number': 'ward_number',
                'ward_cat': 'ward_cat',
                'ward_places': 'ward_places',
                'ward_id': 'ward_id',
                'wards': wards,
                'url': '/patient/diseases'
            }

            return render_template('step5_choose_ward.html', **context)

        if len(wards) == 0:

            return render_template('step5_error.html')

        else:

            context = {
                'ward_number': 'ward_number',
                'ward_cat': 'ward_cat',
                'ward_places': 'ward_places',
                'ward_id': 'ward_id',
                'wards': wards,
                'url': '/patient/info'
            }

            return render_template('step5_choose_ward.html', **context)

    else:
        session['ward_of_patient'] = request.form.get('number_ward')

        return redirect('/patient/info')


# Функция изменения био
@add_patient.route('/edit_bio', methods=['GET', 'POST'])
@login_permission_required
def edit_bio():

    session['stage'] = 12

    if request.method == 'GET':

        context = {
            'name': session.get('patient_info')[0],
            'birthday': session.get('patient_info')[1],
            'passport': session.get('patient_info')[2],
            'address': session.get('patient_info')[3],
            'url': '/patient/info'
        }

        return render_template('step1_add.html', **context)

    else:
        if request.form.get('patient_name') != '':
            session['patient_info'][0] = request.form.get('patient_name')
        if request.form.get('patient_name') != '':
            session['patient_info'][1] = request.form.get('patient_birthday')
        if request.form.get('patient_name') != '':
            session['patient_info'][2] = request.form.get('patient_passport')
        if request.form.get('patient_name') != '':
            session['patient_info'][3] = request.form.get('patient_address')

        return redirect('/patient/info')


# Сохранение кэша
@add_patient.route('/save_cash')
@login_permission_required
def save_cash():

    return redirect('/')


# Очистка кэша
@add_patient.route('/delete_cash')
@login_permission_required
def delete_cash():

    if session.get('stage') is not None:
        session.pop('stage')

    if session.get('search') is not None:
        session.pop('search')

    if session.get('status') is not None:
        session.pop('status')

    if session.get('status_code') is not None:
        session.pop('status_code')

    if session.get('patient_info') is not None:
        session.pop('patient_info')

    if session.get('id_of_patient') is not None:
        session.pop('id_of_patient')

    if session.get('bran_of_patient') is not None:
        session.pop('bran_of_patient')

    if session.get('department_of_patient') is not None:
        session.pop('department_of_patient')

    if session.get('doctor_of_patient') is not None:
        session.pop('doctor_of_patient')

    if session.get('disease_of_patient') is not None:
        session.pop('disease_of_patient')

    if session.get('ward_of_patient') is not None:
        session.pop('ward_of_patient')

    if session.get('history') is not None:
        session.pop('history')

    if session.get('correction_info') is not None:
        session.pop('correction_info')

    return redirect('/')


# Функция занесения пациента и информации в БД
@add_patient.route('/send_to_db')
@login_permission_required
def send_to_db():

    id_of_patient = session.get('id_of_patient')

    status_subcode = 0

    # Новый пациент
    if id_of_patient is None:
        status_subcode = 1

        patient_bio = session.get('patient_info')

        sql = provider.get('get_id_of_new_patient.sql')
        check1 = work_with_db(current_app.config['db_config'], sql)

        # Для новых пациентов без даты рождения
        if patient_bio[1] == '':
            sql = provider.get('add_new_patient_wb.sql',
                               name=patient_bio[0],
                               passport=patient_bio[2],
                               address=patient_bio[3])

        # Для новых пациентов с датой рождения
        else:
            sql = provider.get('add_new_patient.sql',
                               name=patient_bio[0],
                               birthday=patient_bio[1],
                               passport=patient_bio[2],
                               address=patient_bio[3])

        # Создаем нового пациента в базе данных
        make_update(current_app.config['db_config'], sql)

        sql = provider.get('get_id_of_new_patient.sql')
        result = work_with_db(current_app.config['db_config'], sql)

        # Пациент успешно создан - СТАТУС КОД 1
        if result[0]['id'] != check1[0]['id']:
            id_of_patient = result[0]['id']

            print('НОВЫЙ ПАЦИЕНТ УСПЕШНО СОЗДАН')

        # ОШИБКА. Пациент не создан - СТАТУС КОД 5
        else:
            session['status_code'] = 5
            print('ОШИБКА 5')

            return redirect('/patient/final-result')

    status = int(session.get('status'))

    # Занесение пациента без расширенных прав
    if status == 1:

        # Занесение в таблицу ожидания
        sql = provider.get('uncorfimed_patient.sql',
                           patient_id=id_of_patient,
                           doctor_id=session.get('doctor_of_patient'))

        make_update(current_app.config['db_config'], sql)

        # Поиск занесенной информации
        sql = provider.get('check_uncorfimed.sql',
                           id=id_of_patient,
                           doctor=session.get('doctor_of_patient'),
                           date=datetime.today().strftime('%Y-%m-%d'))

        check2 = work_with_db(current_app.config['db_config'], sql)

        # Проверка корректности - СТАТУС КОД 1/2
        if check2[0]['pat_key'] == int(id_of_patient):

            if status_subcode == 0:
                session['status_code'] = 1
            else:
                session['status_code'] = 2

            print('СВЯЗЬ УСПЕШНО СОЗДАНА')

            return redirect('/patient/final-result')

        # ОШИБКА. Связь не создана - СТАТУС КОД 6
        else:

            session['status_code'] = 6
            print('ОШИБКА 6')

            return redirect('/patient/final-result')

    # Занесение пациента с расширенными правами
    if status == 2:

        sql = provider.get('send_to_db.sql',
                           disease=session.get('disease_of_patient'),
                           patient=id_of_patient,
                           doctor=session.get('id_of_doctor'),
                           ward=session.get('ward_of_patient'))

        make_update(current_app.config['db_config'], sql)

        if status_subcode == 0:
            session['status_code'] = 3
        else:
            session['status_code'] = 4

        print('СВЯЗЬ УСПЕШНО СОЗДАНА')

        return redirect('/patient/final-result')


# Окно итогового результата
@add_patient.route('/final-result')
@login_permission_required
def final_result():

    title = [None, None, None]
    url = [None, None]
    button_title = [None, None]

    status_code = int(session.get('status_code'))

    # Пациент из базы данных. Ограниченные права
    if status_code == 1:
        title[0] = 'Успешно'
        title_status = 'Статус: ожидает подтверждения врача'

        button_title[0] = 'Вернуться в главное меню'
        url[0] = '/patient/delete_cash'

        context = {
            'title': title,
            'title_status': title_status,
            'url': url,
            'button_title': button_title,
            'length_title': 1,
            'length_button': 1
        }

        return render_template('result_of_select.html', **context)

    # Новый пациент. Ограниченные права
    if status_code == 2:
        title[0] = 'Пациент'
        title[1] = session.get('patient_info')[0]
        title[2] = 'успешно создан'
        title_status = 'Статус: ожидает подтверждения врача'

        button_title[0] = 'Вернуться в главное меню'
        url[0] = '/patient/delete_cash'

        context = {
            'title': title,
            'title_status': title_status,
            'url': url,
            'button_title': button_title,
            'length_title': 3,
            'length_button': 1
        }

        return render_template('result_of_select.html', **context)

    # Пациент из базы данных. Расширенные права
    if status_code == 3:
        title[0] = 'Успешно'
        title_status = 'Статус: на лечении'

        button_title[0] = 'Вернуться в главное меню'
        url[0] = '/patient/delete_cash'

        context = {
            'title': title,
            'title_status': title_status,
            'url': url,
            'button_title': button_title,
            'length_title': 1,
            'length_button': 1
        }

        return render_template('result_of_select.html', **context)

    # Новый пациент. Расширенные права
    if status_code == 4:
        title[0] = 'Пациент'
        title[1] = session.get('patient_info')[0]
        title[2] = 'успешно создан'
        title_status = 'Статус: на лечении'

        button_title[0] = 'Вернуться в главное меню'
        url[0] = '/patient/delete_cash'

        context = {
            'title': title,
            'title_status': title_status,
            'url': url,
            'button_title': button_title,
            'length_title': 3,
            'length_button': 1
        }

        return render_template('result_of_select.html', **context)

    # ОШИБКА: Пациент не занесен в БД
    if status_code == 5:
        title[0] = 'ПАЦИЕНТ НЕ ЗАНЕСЕН В БАЗУ ДАННЫХ'

        url[0] = '/patient/info'
        url[1] = '/patient/delete_cash'
        button_title[0] = 'Вернуться к карте пациента'
        button_title[1] = 'Вернуться в главное меню'

        context = {
            'title': title,
            'url': url,
            'button_title': button_title,
            'length_title': 1,
            'length_button': 2
        }

        return render_template('result_of_select.html', **context)

    # ОШИБКА: Связь не создана
    if status_code == 6:
        title[0] = 'СВЯЗЬ НЕ СОЗДАНА'

        url[0] = '/patient/info'
        url[1] = '/patient/delete_cash'
        button_title[0] = 'Вернуться к карте пациента'
        button_title[1] = 'Вернуться в главное меню'

        context = {
            'title': title,
            'url': url,
            'button_title': button_title,
            'length_title': 1,
            'length_button': 2
        }

        return render_template('result_of_select.html', **context)
