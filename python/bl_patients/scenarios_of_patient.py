# Сторонние пакеты
from flask import render_template, current_app, session
import numpy

# Модули проекта
from DB.sql_provider import SQLProvider
from DB.database import work_with_db


provider = SQLProvider('sql/notice/')


def patients_scenario_room():

    dep_key = session.get('depart_key_of_doctor')

    sql = provider.get('all_wards.sql', dep_key=dep_key)
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
        headline = ['В ДАННОМ ОТДЕЛЕНИИ', 'НЕТ СВОБОДНЫХ ПАЛАТ']

        context = {
            'headline': headline,
            'length': 2
        }

        return render_template('error.html', **context)

    else:
        context = {
            'ward_number': 'ward_number',
            'ward_cat': 'ward_cat',
            'ward_places': 'ward_places',
            'ward_id': 'ward_id',
            'wards': wards
        }

        return render_template('ward.html', **context)
