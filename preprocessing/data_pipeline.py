from data_cleaner import (open_weird_csv, return_keep_index_regex, return_ingredients_counter, 
                          return_keep_index_occurence, clean_dataset)
from categories_scraper import trouver_moment_sur_series, trouver_nationalite_sur_series


recipes_path = "../data/recipes.csv"

if __name__ == "__main__":
    recipes = open_weird_csv(recipes_path)
