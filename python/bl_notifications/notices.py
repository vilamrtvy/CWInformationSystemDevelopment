def get_headline(number):

    amount = int(number)

    if amount == 0:
        headline = 'НЕТ НОВЫХ ПАЦИЕНТОВ'

    else:
        entry = 'У ВАС '

        if amount == 1:
            close = ' НОВЫЙ ПАЦИЕНТ'

        elif amount >= 2 and amount <= 4:
            close = ' НОВЫХ ПАЦИЕНТА'

        elif amount >= 5 and amount <= 20:
            close = ' НОВЫХ ПАЦИЕНТОВ'

        else:
            modulo = amount % 10

            if modulo == 1:
                close = ' НОВЫЙ ПАЦИЕНТ'

            elif modulo >= 2 and modulo <= 4:
                close = ' НОВЫХ ПАЦИЕНТА'

            else:
                close = ' НОВЫХ ПАЦИЕНТОВ'

        headline = entry + str(amount) + close

    return headline
