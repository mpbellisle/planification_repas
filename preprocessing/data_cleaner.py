from collections import Counter
from csv import reader
import re
import pandas as pd
import numpy as np

from quantity_matching import return_dict_ing_qte

MIN_INGREDIENTS_OCCURENCES = 10


def open_weird_csv(filename):
    with open(filename, "r") as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        df = pd.DataFrame(columns=header[0].split(";"))
        i = 0
        while True:
            try:
                next_row = next(csv_reader)
            except UnicodeDecodeError:
                continue
            except StopIteration:
                break
            if next_row:
                next_row_list = "".join(next_row).split(";")
                if len(next_row_list) == 10:
                    df.loc[i] = next_row_list
                    i += 1
        return df


def return_keep_index_regex(data):
    to_keep_index = []
    for i, row in data.iterrows():
        keep = not re.search("[0-9]|:|'|to taste|\(", row["Ingredients"])
        to_keep_index.append(keep)
    return to_keep_index


def return_ingredients_counter(data):
    all_ingredients = []
    for i, row in data.iterrows():
        all_ingredients.extend(row["ingredients_list"])
    return Counter(all_ingredients)


def return_keep_index_occurence(data, min_occurences):
    ingredients_counter = return_ingredients_counter(data)

    more_than_n_ingredients_list = []
    for ingredient, counter in ingredients_counter.items():
        if counter >= min_occurences:
            more_than_n_ingredients_list.append(ingredient)

    index_to_keep_occurences = []
    for i, row in data.iterrows():
        list_ing = row["ingredients_list"]
        keep = len(set(list_ing) & set(more_than_n_ingredients_list)) == len(set(list_ing))
        index_to_keep_occurences.append(keep)
    return index_to_keep_occurences


def clean_dataset(data):
    data = data[return_keep_index_regex(data)]
    data["ingredients_list"] = data["Ingredients"].apply(lambda row: sorted(list(set(row.lower().split(",")))))
    data = data.drop_duplicates(subset="Recipe Name", keep="first")
    ingredient_counter = return_ingredients_counter(data)
    while np.min(list(ingredient_counter.values())) < MIN_INGREDIENTS_OCCURENCES:
        data = data[return_keep_index_occurence(data, MIN_INGREDIENTS_OCCURENCES)]
        ingredient_counter = return_ingredients_counter(data)

    data = data.reset_index(drop=True)
    data["RecipeID"] = data["RecipeID"].astype(str)
    return data


def get_merge_df(clean_recipes_filename, recipes_filename):
    clean_recipes = pd.read_csv(clean_recipes_filename, sep=";")
    clean_recipes = clean_dataset(clean_recipes)

    recipes = open_weird_csv(recipes_filename)
    recipes_to_merge = recipes.rename(columns={"Ingredients": "quantites"})

    merge_df = clean_recipes.merge(recipes_to_merge[["RecipeID", "quantites"]], how="inner", on="RecipeID")
    merge_df["quantites_list"] = merge_df["quantites"].apply(lambda row: row.lower().replace("'", "").split("**"))

    merge_df["ingredients_quantites"] = merge_df[["quantites_list", "ingredients_list"]].apply(
        lambda row: return_dict_ing_qte(row["quantites_list"], row["ingredients_list"]), axis=1)

    merge_df = merge_df.loc[pd.notna(merge_df["ingredients_quantites"])]
    merge_df = merge_df.reset_index(drop=True)

    return merge_df
