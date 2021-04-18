from preprocessing.data_cleaner import get_merge_df
from preprocessing.categories_scraper import trouver_moment_sur_series, trouver_nationalite_sur_series


recipes_path = "data/recipes.csv"
clean_recipes_path = "data/clean_recipes.csv"
nrows = 200
out_path = f"data/recipes_out_{nrows if nrows else 'full'}.pkl"

if __name__ == "__main__":
    recipes = get_merge_df(clean_recipes_path, recipes_path).sample(nrows)
    print("merged")
    recipes["nationalites"] = trouver_nationalite_sur_series(recipes["Recipe Name"])
    print(recipes["nationalites"])
    recipes["moments"] = trouver_moment_sur_series(recipes["Recipe Name"])
    print(recipes["moments"])
    recipes.to_pickle(out_path)
