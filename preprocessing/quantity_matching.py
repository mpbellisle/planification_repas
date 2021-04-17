import re

MEASURE_MAPPING = {"cup": 250, "tablespoon": 15, "teaspoon": 5, "pinch": 1}


def regex_match_pattern(measure):
    return f"^(.*?)({measure})"


def return_dict_ing_qte(quantites_list, ingredients_list):
    try:
        ing_qte = {}
        qte_list = quantites_list
        for ing in ingredients_list:
            qte = 0
            for qte_string in qte_list:
                if ":" in qte_string:
                    next
                if re.search(ing, qte_string):
                    qte += return_ml_from_string(qte_string)
            if qte == 0:
                for qte_string in qte_list:
                    if re.search(ing, qte_string):
                        qte_str = re.match("^[0-9]+", qte_string)
                        if qte_str:
                            qte += eval(qte_str.group())
            ing_qte[ing] = int(round(qte, 0))
    except:
        ing_qte = None
    return ing_qte


def return_ml_from_string(string):
    qte = 0
    for measure_name, measure_qte in MEASURE_MAPPING.items():
        qte_int = 0
        measure_match = re.match(regex_match_pattern(measure_name), string)
        if measure_match:
            for elem in measure_match.group(1).split(" "):
                if elem:
                    qte_int += eval(elem)
        qte += qte_int*measure_qte
    if "to taste" in string:
        qte += 1
    return qte
