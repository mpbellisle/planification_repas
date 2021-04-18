import pandas as pd

from preprocessing.constant import NATIONALITES, ING_TO_REMOVE, BASE_ING_QTE_MAPPING, AVAILABLE_ING

nrows = 200
processed_recipes_path = "data/recipes_out_200.pkl"
dzn_out_path = f"data/data_recettes_out_{nrows if nrows else 'full'}.dzn"


def format_ingredients(noms_ingredients, dict_ingredients):
    list_out = list()
    for nom in noms_ingredients:
        list_out.append(dict_ingredients.get(nom, 0))
    return list_out


def qtes_et_peremptions(noms_ingredients):
    values_dict = {**BASE_ING_QTE_MAPPING, **AVAILABLE_ING}
    qtes_disponibles_list = list()
    peremptions_list = list()
    for nom in noms_ingredients:
        qtes_disponibles_list.append(values_dict.get(nom, (0,0))[0])
        peremptions_list.append(values_dict.get(nom, (0,0))[1])
    return qtes_disponibles_list, peremptions_list


def add_dzn_2darray_to_lines(lines, titre_array, list_series):
    lines.append(f"{titre_array} = [|{str(list_series[0])[1:-1]},")
    for row in list_series[1:-1]:
        lines.append(f"|{str(row)[1:-1]},")
    lines.append(f"|{str(list_series[len(list_series) - 1])[1:-1]}|];")
    return lines


def add_dzn_1darray_to_lines(lines, titre_array, list):
    lines.append(f"{titre_array} = [{str(list)[1:-1]}];")
    return lines


def format_dzn(recipes):
    lines = list()

    noms_ingredients = set()
    for row in recipes["ingredients_quantites"]:
        noms_ingredients = noms_ingredients.union(set(row.keys()))
    noms_ingredients = sorted(list(noms_ingredients))
    ingredients_list_series = recipes["ingredients_quantites"].apply(lambda dict: format_ingredients(noms_ingredients, dict))
    noms_recettes = recipes["Recipe Name"].tolist()
    noms_moments = ["breakfast", "lunch", "dinner"]
    # On considère toutes les recettes comme étant acceptables pour dîner
    moments_list_series = recipes["moments"].apply(lambda x: [int(x[0]), 1, int(x[1])])
    noms_nationalites = NATIONALITES
    qtes_disponibles_list, peremptions_list = qtes_et_peremptions(noms_ingredients)

    lines.append(f"nb_recettes = {len(recipes)};")
    lines.append(f"nb_ingredients = {len(noms_ingredients)};")
    lines.append(f"nb_moments = {len(noms_moments)};")
    lines.append(f"nb_nationalites = {len(noms_nationalites)};")
    lines.append("")
    lines.append("")

    lines.append("% Noms des ingredients:")
    lines.append(f"% {noms_ingredients}")
    lines.append("")
    lines = add_dzn_2darray_to_lines(lines, "ingredients", ingredients_list_series)
    lines.append("")
    lines = add_dzn_1darray_to_lines(lines, "qtes_disponibles", qtes_disponibles_list)
    lines.append("")
    lines = add_dzn_1darray_to_lines(lines, "peremptions", peremptions_list)
    lines.append("")
    lines.append("")

    lines.append("% Noms des recettes:")
    lines.append(f"% {noms_recettes}")
    lines.append("")

    lines.append("% Noms des moments:")
    lines.append(f"% {noms_moments}")
    lines.append("")
    lines = add_dzn_2darray_to_lines(lines, "moments", moments_list_series)
    lines.append("")
    lines.append("")

    lines.append("% Noms des nationalites:")
    lines.append(f"% {noms_nationalites}")
    lines.append("")
    lines = add_dzn_2darray_to_lines(lines, "nationalites", recipes["nationalites"].apply(lambda l: [int(e) for e in l]))
    lines.append("")
    lines = add_dzn_1darray_to_lines(lines, "preferences_nationalites", [0] * len(noms_nationalites))
    lines.append("")

    return lines


def write_lines(lines, out_path):
    fichier = open(out_path,"w")
    for i in range(len(lines)):
        lines[i] += "\n"
    fichier.writelines(lines)
    fichier.close()


if __name__ == "__main__":
    recipes = pd.read_pickle(processed_recipes_path).sample(nrows).reset_index(drop=True)
    lines = format_dzn(recipes)
    write_lines(lines, dzn_out_path)
