from data_cleaner import get_merge_df
from categories_scraper import trouver_moment_sur_series, trouver_nationalite_sur_series


recipes_path = "../data/recipes.csv"
clean_recipes_path = "../data/clean_recipes.csv"
out_path = "../data/recipes_out.pkl"
nrows = 1000

if __name__ == "__main__":
    recipes = get_merge_df(clean_recipes_path, recipes_path).head(nrows)
    print("merged")
    recipes["nationalites"] = trouver_nationalite_sur_series(recipes["Recipe Name"])
    print(recipes["nationalites"])
    recipes["moments"] = trouver_moment_sur_series(recipes["Recipe Name"])
    print(recipes["moments"])
    recipes.to_pickle(out_path)
