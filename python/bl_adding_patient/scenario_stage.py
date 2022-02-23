def searching_stage_of_user(stage):

    scenario_stage = {
        None: '/patient/main_menu',
        2: '/patient/founded_patients',
        3: '/patient/founded_patient',
        4: '/patient/brans',
        5: '/patient/doctors',
        6: '/patient/diseases',
        7: '/patient/ward',
        8: '/patient/info',
        9: '/patient/edit_disease_or_ward',
        10: '/patient/edit_disease',
        11: '/patient/edit_ward',
        12: '/patient/edit_bio'
    }
    scenario = scenario_stage.get(stage)
    return scenario

