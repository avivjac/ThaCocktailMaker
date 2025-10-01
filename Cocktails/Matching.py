import requests


# API

# the function get ingrdeint and match a random cocktail with the ingredient, which the user have all the ingredients
def find_random_cocktail_by_ingredient(main_ingredient):
    data = find_cocktails_by_ingredient(main_ingredient)
    user_ingredients = []

    for cocktail in data:
        details = get_cocktail_details(cocktail['idDrink'])
        ingredients = []
        i=0
        for i in range(1,12):
            ingredient = details.get(f"strIngredient{i}")
            ingredients.append(ingredient)
            measure = details.get(f"strMeasure{i}")
            if ingredient and measure:
                print(f"Ingredient {i}: {ingredient} - {measure}")


        # גישה לדאטה בייס לבדוק איזה מרכיבים יש למשתמש
        

def find_cocktails_by_ingredient(main_ingredient):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={main_ingredient}"
    response = requests.get(url)
    data = response.json()
    # print(data)
    return data['drinks']

def get_cocktail_details(cocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}"
    response = requests.get(url)
    data = response.json()
    print(data)
    if data['drinks'] is None:
        return None
    
    return data['drinks'][0]
    

if __name__ == "__main__":
    main_ingredient = "gin"
    cocktails = find_random_cocktail_by_ingredient(main_ingredient)
    # print(cocktails)

    # cocktail = get_cocktail_details("11007")


# Database




