MEASURE_MAPPING = {"cup": 250, "tablespoon": 15, "teaspoon": 5, "pinch": 1}

NATIONALITES = ("american", "mexican", "french", "canadian", "japanese", "chinese", "korean", "portuguese", "spanish", "polish")

ING_TO_REMOVE = [
    "bake",
    "cake",
    "chill",
    "cocktail",
    "hamburger",
    "kosher",
    "low fat",
    "fat free",
    "meat",
    "muffin",
    "shortening",
    "herb"
]


BASE_ING_QTE_MAPPING = {
    "water": (10000, 10000),
    "pepper": (10000, 10000),
    "sugar": (10000, 10000),
    "oil": (10000, 10000),
    "flour": (10000, 10000),
    "ice": (10000, 10000),
    "paprika": (10000, 10000),
    "salt": (10000, 10000),
    "seed": (10000, 10000),
    "sesame": (10000, 10000),
    "skewer": (10000, 10000),
    "sodium": (10000, 10000),
    "baking mix": (10000, 10000),
    "baking powder": (10000, 10000),
    "baking soda": (10000, 10000),
    "honey": (10000, 10000),
}


AVAILABLE_ING = {
    "chicken": (10, 5),
    "egg": (12, 14),
    "milk": (2000, 8),
    "orange": (5, 10),
    "onion": (10, 20),
    "mushroom": (500, 20),
    "butter": (1000, 60),
    "ham": (600, 10),
    "garlic": (250, 20),
    "cheddar": (500, 18),
    "mayonnaise": (800, 60),
    "mozarella": (300, 24),
    "parmesan": (150, 21),
    "sausage": (450, 4),
}