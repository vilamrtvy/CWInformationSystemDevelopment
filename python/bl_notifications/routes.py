# Сторонние пакеты
from flask import Blueprint, render_template, session, request, current_app, redirect
import numpy

# Модули проекта
from access import login_permission_required
from DB.sql_provider import SQLProvider
from DB.database import work_with_db, make_update
from bl_adding_patient.diseases import all_diseases
from bl_notifications.notices import get_headline


notifications = Blueprint('notice', __name__, template_folder='templates')
provider = SQLProvider('sql/notice/')


# Функция добавления основной информации
@notifications.route('/', methods=['GET', 'POST'])
@login_permission_required
def all_notices():

    # Страница уведомлений врача
    if request.method == 'GET':

        sql = provider.get('notices_of_doctor.sql',
                           id=session.get('id_of_doctor'))

        notification_list = work_with_db(current_app.config['db_config'], sql)

        notices = len(notification_list)
        headline = get_headline(notices)

        if not notification_list:
            header = [headline]

            context = {
                'headline': header,
                'length': 1
            }

            return render_template('error.html', **context)

        else:
            res_keys = ['pat_name', 'pat_birthday', 'pat_passport',
                        'pat_address', 'rec_date']

            status = 'ОЖИДАЕТ ПОДТВЕРЖДЕНИЯ'

            keylist = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'ПАСПОРТ',
                       'АДРЕС', 'ДАТА ПОСТУПЛЕНИЯ', 'СТАТУС']

            context = {
                'headline': headline,
                'keylist': keylist,
                'list': notification_list,
                'res_keys': res_keys,
                'status': status
            }

            return render_template('notices.html', **context)

    # Занесение информации в сессию
    else:

        patient_id = request.form.get('patient')
        s_id = session.get('patient_notification_id')

        if s_id is None:
            session['patient_notification_id'] = patient_id
            return redirect('/notice/patient')

        elif s_id is not None and s_id == patient_id:
            return redirect('/notice/patient')

        else:
            session['patient_notification_id'] = patient_id
            if session.get('disease') is not None:
                session.pop('disease')
            if session.get('ward') is not None:
                session.pop('ward')
            return redirect('/notice/patient')


# Карта пациента
@notifications.route('/patient')
@login_permission_required
def notice_patient():
    id_patient = session.get('patient_notification_id')

    # Информация о пациента
    sql = provider.get('patient_info.sql', id=id_patient)
    result = work_with_db(current_app.config['db_config'], sql)

    patient = [result[0]['pat_name'], result[0]['pat_birthday'],
               result[0]['pat_passport'], result[0]['pat_address']]

    title_list = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'НОМЕР ПАСПОРТА', 'АДРЕС ПРОЖИВАНИЯ']

    # История болезни пациента
    sql = provider.get('patient_history.sql',
                       pat_id=id_patient,
                       doc_id=session.get('id_of_doctor'))
    result = work_with_db(current_app.config['db_config'], sql)

    session['id_of_history'] = result[0]['his_id']

    history = [result[0]['rec_date'], '',
               result[0]['bran_name'], '',
               result[0]['doc_name'], 'В ОБРАБОТКЕ']

    if session.get('disease') is not None:
        history[1] = session.get('disease')

    if session.get('ward') is not None:
        sql = provider.get('number_of_ward.sql',
                           ward=session.get('ward'))
        result = work_with_db(current_app.config['db_config'], sql)
        history[3] = result[0]['ward_number']

    history_list = ['ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ', 'ОТДЕЛЕНИЕ',
                    '№ ПАЛАТЫ', 'ЛЕЧАЩИЙ ВРАЧ', 'СТАТУС']

    context = {
        'title_list': title_list,
        'patient': patient,
        'history_list': history_list,
        'history': history
    }

    return render_template('patient_card.html', **context)


# Окно выбора добавления диагноза или номера палаты
@notifications.route('/adding')
@login_permission_required
def adding_info():

    return render_template('adding_d_w.html')


# Функция добавления диагноза
@notifications.route('/add-disease', methods=['GET', 'POST'])
@login_permission_required
def adding_disease():

    if request.method == 'GET':

        diseases = all_diseases(session.get('depart_key_of_doctor'))

        length = len(diseases) / 3

        context = {
            'length': int(length),
            'list_of_diseases': diseases,
            'url': '/patient/info'
        }

        return render_template('add_disease.html', **context)

    else:
        session['disease'] = request.form.get('disease')

        if session.get('ward') is None:
            return redirect('/notice/adding')

        else:
            return redirect('/notice/patient')


# Функция добавления палаты
@notifications.route('/add-ward', methods=['GET', 'POST'])
@login_permission_required
def adding_ward():

    if request.method == 'GET':

        dep_key = session.get('depart_key_of_doctor')

        sql = provider.get('all_wards.sql', dep_key=dep_key)
        wards = work_with_db(current_app.config['db_config'], sql)

        sql = provider.get('busy_wards.sql', dep_key=dep_key)
        busy = work_with_db(current_app.config['db_config'], sql)

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
            headline = ['В ДАННОМ ОТДЕЛЕНИИ', 'НЕТ СВОБОДНЫХ ПАЛАТ']

            context = {
                'headline': headline,
                'length': 2
            }

            return render_template('notice_error.html', **context)

        else:
            context = {
                'ward_number': 'ward_number',
                'ward_cat': 'ward_cat',
                'ward_places': 'ward_places',
                'ward_id': 'ward_id',
                'wards': wards
            }

            return render_template('add_ward.html', **context)

    else:
        session['ward'] = request.form.get('number_ward')

        return redirect('/notice/patient')


# Обновляем в базе данных
@notifications.route('/accept')
@login_permission_required
def update_patient_history():

    if session.get('ward') is None:
        reason = ['ВЫ НЕ ВЫБРАЛИ ПАЛАТУ']
        url = ['/notice/add-ward']
        button_name = ['ВЫБРАТЬ ПАЛАТУ']

        context = {
            'reason': reason,
            'length1': 1,
            'url': url,
            'button_name': button_name,
            'length2': 1
        }

        return render_template('notice_no_data.html', **context)

    elif session.get('disease') is None:

        sql = provider.get('update_info.sql',
                           disease=' ',
                           ward=int(session.get('ward')),
                           his_id=int(session.get('id_of_history')))

        make_update(current_app.config['db_config'], sql)

        session.pop('ward')

        return redirect('/')

    else:

        sql = provider.get('update_info.sql',
                           disease=session.get('disease'),
                           ward=int(session.get('ward')),
                           his_id=int(session.get('id_of_history')))

        make_update(current_app.config['db_config'], sql)

        session.pop('disease')
        session.pop('ward')

        return redirect('/')
