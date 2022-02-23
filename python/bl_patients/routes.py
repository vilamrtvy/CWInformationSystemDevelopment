# Сторонние пакеты
from flask import Blueprint, render_template, request, current_app, redirect, session

# Модули проекта
from access import login_permission_required
from DB.sql_provider import SQLProvider
from DB.database import work_with_db, make_update
from bl_adding_patient.diseases import all_diseases
from bl_patients.scenarios_of_patient import patients_scenario_room


patients_cards = Blueprint('cards', __name__, template_folder='templates')
provider = SQLProvider('sql/request/')


# Страница с пациентами врача
@patients_cards.route('/', methods=['GET', 'POST'])
@login_permission_required
def all_patients():
    if request.method == 'GET':
        doctor_id = session.get('id_of_doctor')

        sql = provider.get('requests_patients.sql', doc_id=doctor_id)
        result = work_with_db(current_app.config['db_config'], sql)

        if not result:
            headline = ['ПАЦИЕНТЫ НЕ НАЙДЕНЫ']

            context = {
                'headline': headline,
                'length': 1
            }

            return render_template('error.html', **context)

        else:
            res_keys = list(result[0].keys())
            del res_keys[0], res_keys[4]

            for i in range(0, len(result)):
                if result[i]['count_dis'] != result[i]['count_rec']:
                    result[i]['count_dis'] = 'НА ЛЕЧЕНИИ'
                else:
                    result[i]['count_dis'] = 'ВЫПИСАН'

            keylist = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'ПАСПОРТ', 'СТАТУС']
            context = {
                'list': result,
                'res_keys': res_keys,
                'keylist': keylist
            }

            return render_template("patients.html", **context)
    else:
        session['request_id_of_patient'] = request.form.get("patient", "")

        return redirect('/cards/about-patient')


# Медицинская карта пациента
@patients_cards.route('/about-patient')
@login_permission_required
def about_patient():
    id_patient = session.get('request_id_of_patient')

    # Информация о пациента
    sql = provider.get('request_about_patient.sql', pat_id=id_patient)
    patient = work_with_db(current_app.config['db_config'], sql)

    session['request_name'] = patient[0]['pat_name']

    title_list = ['ФИО', 'ДАТА РОЖДЕНИЯ', 'НОМЕР ПАСПОРТА', 'АДРЕС ПРОЖИВАНИЯ']

    info_list = [patient[0]['pat_name'], patient[0]['pat_passport'],
                 patient[0]['pat_birthday'], patient[0]['pat_address']]

    # История болезней пациента
    sql = provider.get('request_history_of_patient.sql', pat_id=id_patient)
    history = work_with_db(current_app.config['db_config'], sql)

    res_keys = list(history[0].keys())
    del res_keys[0]

    status_of_patient = 0

    for i in range(0, len(history)):
        if history[i]['dis_date'] is None:
            if session.get('access_rights') == 'mrg':
                status_of_patient = 2
            elif history[i]['doc_name'] == session.get('name_of_doctor'):
                status_of_patient = 1
            else:
                status_of_patient = 0

            history[i]['dis_date'] = 'На лечении'
            session['history_id'] = history[i]['his_id']

            if history[i]['rec_diag'] == ' ':
                history[i]['rec_diag'] = 'НЕ ПОСТАВЛЕН'

    keylist = ['ДАТА ПОСТУПЛЕНИЯ', 'ДИАГНОЗ', 'ДАТА ВЫПИСКИ', 'ОТДЕЛЕНИЕ',
               '№ ПАЛАТЫ', 'ЛЕЧАЩИЙ ВРАЧ']

    context = {
        'history': history,
        'res_keys': res_keys,
        'keylist': keylist,
        'title_list': title_list,
        'info_list': info_list
    }

    if status_of_patient == 1 or status_of_patient == 2:
        return render_template("about_patient.html", **context)

    else:
        return render_template("about_patient_wd.html", **context)


# Окно выбора изменения диагноза или номера палаты
@patients_cards.route('/wanna-edit')
@login_permission_required
def wanna_edit():

    return render_template('wanna_edit.html')



# Изменение диагноза
@patients_cards.route('/edit-disease', methods=['GET', 'POST'])
@login_permission_required
def patient_disease_edit():

    if request.method == 'GET':

        diseases = all_diseases(session.get('depart_key_of_doctor'))

        length = len(diseases) / 3

        context = {
            'length': int(length),
            'list_of_diseases': diseases
        }

        return render_template('disease.html', **context)

    else:
        disease = request.form.get('disease')
        his_id = session.get('history_id')

        sql = provider.get('update_disease.sql',
                           disease=disease,
                           his_id=his_id)
        make_update(current_app.config['db_config'], sql)

    return redirect('/cards/about-patient')


# Изменения номера палаты
@patients_cards.route('/edit-patient-room', methods=['GET', 'POST'])
@login_permission_required
def patient_room_edit():

    if request.method == 'GET':

        patient_scenario_edit = {
            'ward': patients_scenario_room
        }
        scenario = patient_scenario_edit.get('ward')

        return scenario()

    else:
        print('here')
        ward = request.form.get('number_ward')
        his_id = session.get('history_id')

        sql = provider.get('update_ward.sql',
                           ward=ward,
                           his_id=his_id)
        make_update(current_app.config['db_config'], sql)

        return redirect('/cards/about-patient')


# Подтверждение выписки
@patients_cards.route('confirmation')
@login_permission_required
def confirm_discharge():

    if session.get('history_id') is None:
        headline = ['ВЫ НЕ ВЫБРАЛИ ПАЦИЕНТА']

        context = {
            'headline': headline,
            'length': 1
        }

        return render_template('error.html', **context)

    else:

        return render_template('total_accept.html',
                               name=session.get('request_name'))


# Выписка пациента
@patients_cards.route('discharge-patient')
@login_permission_required
def discharge_patient():

    his_id = session.get('history_id')

    sql = provider.get('discharge_patient.sql', his_id=his_id)
    make_update(current_app.config['db_config'], sql)

    return render_template('patient_is_discharged.html',
                           name=session.get('request_name'))


# Возврат в главное меню
@patients_cards.route('/go-home')
@login_permission_required
def go_home():

    if session.get('request_id_of_patient') is not None:
        session.pop('request_id_of_patient')

    if session.get('history_id') is not None:
        session.pop('history_id')

    return redirect('/')
