def post_function(bran_name, gender, post):
    title = None
    title1 = None
    title2 = None
    start_of_title = None

    # Для врачей и заместителей отделения
    if post == 'dc' or post == 'mrg':
        if gender == 'w':
            image = 'url(/static/image/img_woman.png)'
        else:
            image = 'url(/static/image/img_man.png)'

        if bran_name == 101:
            title1 = "ВРАЧ-КАРДИОЛОГ"

        if bran_name == 102:
            title1 = "ВРАЧ-АЛЛЕРГОЛОГ"

        if bran_name == 103:
            title1 = "ВРАЧ-ГАСТРОЭНТЕРОЛОГ"

        if bran_name == 104:
            title1 = "ВРАЧ-ЭНДОКРИНОЛОГ"

        if bran_name == 105:
            if gender == 'w':
                title1 = "ВРАЧ-ГИНЕКОЛОГ"
            else:
                title1 = "ВРАЧ-УРОЛОГ"

        if bran_name == 106:
            title1 = "ВРАЧ-НЕВРОЛОГ"

        if bran_name == 107:
            title1 = "ВРАЧ-ОНКОЛОГ"

        if bran_name == 108:
            title1 = "ВРАЧ-ТРАВМАТОЛОГ-ОРТОПЕД"

        if bran_name == 109:
            title1 = "ВРАЧ-ТЕРАПЕВТ"

        if bran_name == 110:
            title1 = "ВРАЧ-ИНФЕКЦИОНИСТ"

        if bran_name == 113:
            title1 = "ВРАЧ-ПСИХИАТР"

        if bran_name == 112:
            title1 = "ВРАЧ-РЕАНИМАТОЛОГ"

    # Для заместителей отделения
    if post == 'mrg':
        if gender == 'w':
            start_of_title = 'ЗАВЕДУЮЩАЯ'
        else:
            start_of_title = 'ЗАВЕДУЮЩИЙ'

        if bran_name == 101:
            title = "ОТДЕЛЕНИЕМ КАРДИОЛОГИИ"

        if bran_name == 102:
            title = "ОТДЕЛЕНИЕМ АЛЛЕРГОЛОГИИ"

        if bran_name == 103:
            title = "ОТДЕЛЕНИЕМ ГАСТРОЭНТЕРОЛОГИИ"

        if bran_name == 104:
            title = "ОТДЕЛЕНИЕМ ЭНДОКРИНОЛОГИИ"

        if bran_name == 105:
            title = "ОТДЕЛЕНИЕМ ГИНЕКОЛОГИИ И УРОЛОГИИ"

        if bran_name == 106:
            title = "ОТДЕЛЕНИЕМ НЕВРОЛОГИИ"

        if bran_name == 107:
            title = "ОТДЕЛЕНИЕМ ОНКОЛОГИИ"

        if bran_name == 108:
            title = "ОТДЕЛЕНИЕМ ТРАВМАТОЛОГИИ И ОРТОПЕДИИ"

        if bran_name == 109:
            title = "ОТДЕЛЕНИЕМ ТЕРАПЕВТИИ"

        if bran_name == 110:
            title = "ИНФЕКЦИОННЫМ ОТДЕЛЕНИЕМ"

        if bran_name == 113:
            title = "ОТДЕЛЕНИЕМ ПСИХИАТРИИ"

        if bran_name == 112:
            title = "ОТДЕЛЕНИЕМ РЕАНИМАЦИИ"

        title2 = start_of_title + ' ' + title

    if post == 'dc':
        position = [title1]
    if post == 'mrg':
        position = [title1, title2]

    # Для секретарей
    if post == 'scr':
        position = ['СЕКРЕТАРЬ ПРИЕМНОГО ОТДЕЛЕНИЯ']
        image = 'url(/static/image/img_scr.png)'


    return [position, image]
