from django.shortcuts import render
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def fuzzy(str1, str2):
    fuzzy_input1 = str1
    fuzzy_input2 = str2

    person = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'person importance')
    reason = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'reason importance')
    important = ctrl.Consequent(np.arange(0, 101, 1), 'percentage important')

    person['NOT IMPORTANT'] = fuzz.trimf(person.universe, [0, 0, 0.25])
    person["SLIGHTLY IMPORTANT"] = fuzz.trimf(person.universe, [0, 0.25, 0.5])
    person["IMPORTANT"] = fuzz.trimf(person.universe, [0.25, 0.5, 0.75])
    person["FAIRLY IMPORTANT"] = fuzz.trimf(person.universe, [0.5, 0.75, 1])
    person["VERY IMPORTANT"] = fuzz.trimf(person.universe, [0.75, 1, 1])

    reason['NOT IMPORTANT'] = fuzz.trimf(reason.universe, [0, 0, 0.25])
    reason["SLIGHTLY IMPORTANT"] = fuzz.trimf(reason.universe, [0, 0.25, 0.5])
    reason["IMPORTANT"] = fuzz.trimf(reason.universe, [0.25, 0.5, 0.75])
    reason["FAIRLY IMPORTANT"] = fuzz.trimf(reason.universe, [0.5, 0.75, 1])
    reason["VERY IMPORTANT"] = fuzz.trimf(reason.universe, [0.75, 1, 1])

    important["NOT IMPORTANT"] = fuzz.trimf(important.universe, [0, 0, 25])
    important["SLIGHTLY IMPORTANT"] = fuzz.trimf(important.universe, [0, 25, 50])
    important["IMPORTANT"] = fuzz.trimf(important.universe, [25, 50, 75])
    important["FAIRLY IMPORTANT"] = fuzz.trimf(important.universe, [50, 75, 100])
    important["VERY IMPORTANT"] = fuzz.trimf(important.universe, [75, 100, 100])

    rule1 = ctrl.Rule(person['NOT IMPORTANT'] | reason['NOT IMPORTANT'], important['NOT IMPORTANT'])
    rule2 = ctrl.Rule(person['SLIGHTLY IMPORTANT'] | reason['SLIGHTLY IMPORTANT'], important['SLIGHTLY IMPORTANT'])
    rule3 = ctrl.Rule(person['IMPORTANT'] | reason['IMPORTANT'], important['IMPORTANT'])
    rule4 = ctrl.Rule(person['FAIRLY IMPORTANT'] | reason['FAIRLY IMPORTANT'], important['FAIRLY IMPORTANT'])
    rule5 = ctrl.Rule(person['VERY IMPORTANT'] | reason['VERY IMPORTANT'], important['VERY IMPORTANT'])

    important_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

    importing = ctrl.ControlSystemSimulation(important_ctrl)

    importing.input['person importance'] = fuzzy_input1
    importing.input['reason importance'] = fuzzy_input2

    importing.compute()
    fuzzy_result = importing.output['percentage important']

    # print("Importance Percentage:", fuzzy_result, "%")
    # important.view(sim=importing)

    return fuzzy_result

    # if fuzzy_result > 75:
    #     time_frame=3
    #
    # elif fuzzy_result > 45 and fuzzy_result <= 75:
    #     time_frame = 10
    # else:
    #     return 0
