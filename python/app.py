# Стандартные пакеты
import json

# Сторонние пакеты
from flask import Flask, render_template, session, current_app, redirect

# Модули проекта
from bl_authorization.routes import auth
from bl_adding_patient.routes import add_patient
from bl_notifications.routes import notifications
from bl_patients.routes import patients_cards
from bl_reporting.routes import reporting
from DB.sql_provider import SQLProvider
from DB.database import work_with_db
from access import login_permission_required


app = Flask(__name__)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(add_patient, url_prefix='/patient')
app.register_blueprint(reporting, url_prefix='/requests')
app.register_blueprint(patients_cards, url_prefix='/cards')
app.register_blueprint(notifications, url_prefix='/notice')

provider = SQLProvider('sql/')
provider_notices = SQLProvider('sql/notice')

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['db_config'] = json.load(open('configs/db.json', 'r'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json', 'r'))


# Главная страница

@app.route('/')
@login_permission_required
def base_page():

    scenario_factory = {
        None: function_unauthorized,
        'dc': function_dc,
        'mrg': function_mrg,
        'scr': function_scr
    }

    scenario = scenario_factory.get(session.get('access_rights'))

    return scenario()


# Неавторизованный пользователь
def function_unauthorized():
    return render_template('base_for_not_auth.html')


# Пользователь - доктор
def function_dc():
    sql = provider_notices.get('notices_of_doctor.sql',
                               id=session.get('id_of_doctor'))

    result = work_with_db(current_app.config['db_config'], sql)
    notices = len(result)

    session['notices'] = notices

    if notices == 0:
        return render_template('base_for_dc.html')
    else:
        return render_template('base_for_dc.html', amount=notices)


# Пользователь - заведующая/ий отделением
def function_mrg():
    sql = provider_notices.get('notices_of_doctor.sql',
                               id=session.get('id_of_doctor'))

    result = work_with_db(current_app.config['db_config'], sql)
    notices = len(result)

    session['notices'] = notices

    if notices == 0:
        return render_template('base_for_mrg.html')
    else:
        return render_template('base_for_mrg.html', amount=notices)


# Пользователь - заведующая/ий отделением
def function_scr():
    return render_template('base_for_scr.html')


# Выход из аккаунта
@app.route('/end')
@login_permission_required
def end_page():
    session.clear()
    return redirect('/')


# Main функция
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5033)
