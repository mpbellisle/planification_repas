import pandas as pd
from time import sleep
from urllib.request import urlopen, Request


USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
NATIONALITES = ("american", "mexican", "french", "canadian", "japanese", "chinese", "korean", "portuguese", "spanish", "polish")


def trouver_categories(question, plat, categories, nb_pages=1, seuil_proportion=None):
    seuil_proportion = 1 / len(categories) if seuil_proportion is None else seuil_proportion
    question_clean = question.replace(" ", "+")
    plat_clean = plat.lower().replace(" i ", " ").replace(" ", "-").replace("recipe", "")
    URLS = [f"https://www.bing.com/search?q={question_clean}+{plat_clean}&first={i * 10}" for i in range(nb_pages)]
    contenu = str()
    for URL in URLS:
        try:
            req = Request(URL, headers={"User-Agent": USER_AGENT})
            page = urlopen(req)
            contenu += str(page.read()).lower()
        except:
            pass
        sleep(5)
    occurences = tuple(contenu.count(categorie) for categorie in categories)
    occurences_totales = max(sum(occurences), 1)
    categories_bools = [occurences[i] / occurences_totales >= seuil_proportion for i in range(len(categories))]
    return categories_bools


def trouver_categories_sur_series(question, series, categories, nb_pages=1, seuil_proportion=None):
    return series.apply(lambda x: trouver_categories(question, x, categories, nb_pages, seuil_proportion))


def trouver_moment_sur_series(series):
    return trouver_categories_sur_series("what meal is", series, ("breakfast", "dinner"), 1)


def trouver_nationalite_sur_series(series):
    return trouver_categories_sur_series("what nationality is", series, NATIONALITES, 1)


if __name__ == "__main__":
    test = pd.Series(["pizza", "spaghetti", "tacos", "lasagna", "cereal", "hot dog"])
    print(trouver_moment_sur_series(test))
    print(trouver_nationalite_sur_series(test))
