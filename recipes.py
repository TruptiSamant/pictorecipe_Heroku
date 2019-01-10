import requests
import pandas as pd
from config import Spoonacular_API_key
import os
import glob


'''
Get the remaining limit
'''
def getremainigAPIcalls():
    for key in Spoonacular_API_key:
        response = requests.post("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/cuisine",
        headers={
            "X-RapidAPI-Key": key,
            "Content-Type": "application/x-www-form-urlencoded"
            },
            params={
            "ingredientList": "",
            "title": ""
            }
            )
        try:
            calls_remaning = response.headers['X-RateLimit-requests-Remaining']
        except:
            print("move on")

        if (int(calls_remaning) > 0):
            return key

    return None

'''
getRecipeByUrl : query spoonacular API with the link
Return: Return the request
'''
def getRecipeByUrl(url):
    payload = {
        'fillIngredients': True,
        'url': url,
        'limitLicense': True,
        'number': 2,
        'ranking': 1
    }

    # Check if any limit left
    key = getremainigAPIcalls()
    if (key):
        api_key = key
    else:
        return None

    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/extract"

    headers={
        "X-RapidAPI-Key": api_key
    }

    #send the request
    result = requests.get(endpoint, params=payload, headers=headers)

    return result


'''
getRecipe : get the recipe and send it to the routes
Return: Return the request
'''
def getRecipe(cuisine, ingredients):

    #get the ingredients whoes recipes we have saved
    df = pd.read_csv(os.path.join('recipes', 'recipes.csv'), skipinitialspace=True)

    corn_df = df[df['Indian'].str.contains("corn")]
    recipe_link_list = [row['Indian'] for index, row in corn_df.iterrows()]

    print(recipe_link_list[0])

    #make a API call and get the recipe
    result = getRecipeByUrl(recipe_link_list[0])
    print(result)
    #store the information
    recipe_list = []
    info = {}
    try:
        info = {'title': result.json()['title'],
                'sourceUrl': result.json()['sourceUrl'],
                'cookingMinutes': result.json()['cookingMinutes'],
                'image': result.json()['image'],
                'instructions': result.json()['instructions'],
                'ingredients' : [key['originalString'] for key in result.json()['extendedIngredients']]
                }
    except:
        print("Recipe not found")

    recipe_list.append(info)

    print(recipe_list)

    return recipe_list

# getRecipe('Indian', 'Tomato')

def getdict():
    return [{'title': 'spinach corn sandwich',
    'sourceUrl': 'https://hebbarskitchen.com/spinach-corn-sandwich-recipe/',
    'cookingMinutes': 10,
    'image': 'https://spoonacular.com/recipeImages/1047695-556x370.jpg',
    'instructions': 'Instructionsfirstly, in a large tawa heat 1 tsp butter and saute 2 tbsp onion.',
    'ingredients': ['1 tsp butter', '2 tbsp onion finely chopped', '1 cup palak / spinach finely chopped']},
    {'title': 'spinach corn sandwich',
    'sourceUrl': 'https://hebbarskitchen.com/spinach-corn-sandwich-recipe/',
    'cookingMinutes': 10,
    'image': 'https://spoonacular.com/recipeImages/1047695-556x370.jpg',
    'instructions': 'Instructionsfirstly, in a large tawa heat 1 tsp butter and saute 2 tbsp onion.',
    'ingredients': ['1 tsp butter', '2 tbsp onion finely chopped', '1 cup palak / spinach finely chopped']}]

print(Spoonacular_API_key)
