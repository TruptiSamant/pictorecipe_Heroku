import requests
import pandas as pd
from config import Spoonacular_API_key
import os
import glob

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

    api_key = Spoonacular_API_key

    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/extract"

    headers={
        "X-RapidAPI-Key": api_key
    }

    r = requests.get(endpoint, params=payload, headers=headers)
    return r


'''
getRecipe : get the recipe and send it to the routes
Return: Return the request
'''
def getRecipe(cuisine, ingredients):

    #get the ingredients whoes recipes we have saved
    df = pd.read_csv(os.path.join('recipes', 'recipes.csv'), skipinitialspace=True)

    corn_df = df[df['Indian'].str.contains("corn")]
    print(corn_df)

    # indianRecipes_df = pd.read_csv(os.path.join('recipes', cuisine + '.csv'))
    # print(indianRecipes_df[ingredients])
    # cuisines_list = glob.glob("recipes/*.csv")
    # cuisines_df = pd.read_csv(cuisines_list[0])
        # cuisines = []
        # for cuisine in cuisines_list:
        #     a = cuisine.split("\\")[-1:]
        #     b = a[0].split(".")[0:1]
        #     cuisines.append(b[0])
    # else:
    #     return False
    return True

getRecipe('Indian', 'Tomato')
