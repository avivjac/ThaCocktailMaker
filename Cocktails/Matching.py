import requests

def find_random_cocktail_by_ingredient(main_ingredient):
    data = find_cocktails_by_ingredient(main_ingredient)

    for cocktail in data:
        details = get_cocktail_details(cocktail['idDrink'])

        
        # גישה לדאטה בייס לבדוק איזה מרכיבים יש למשתמש
        


def find_cocktails_by_ingredient(main_ingredient):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={main_ingredient}"
    response = requests.get(url)
    data = response.json()
    
    return data['drinks']

def get_cocktail_details(cocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}"
    response = requests.get(url)
    data = response.json()

    if data['drinks'] is None:
        return None
    
    return data['drinks'][0]
    

if __name__ == "__main__":
    main_ingredient = "gin"
    cocktails = find_random_cocktail_by_ingredient(main_ingredient)
    print(cocktails)