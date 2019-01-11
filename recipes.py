import requests
import pandas as pd

import os
import glob
import itertools
# from boto.s3.connection import S3Connection

# def get_key_prod():
#     API_KEYS = S3Connection(os.environ['Spoonacular_API_key1'], os.environ['Spoonacular_API_key1'])
#     print(s3)
is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    print(app.config.from_envvar('Spoonacular_API_key1', silent=True))
else:
    from config import Spoonacular_API_key

'''
Get the remaining limit
'''
def getremainigAPIcalls():
    #loop through API keys
    for key in Spoonacular_API_key:
        #make tiny request
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
            tiny_calls_remaning = response.headers['x-ratelimit-tinyrequests-remaining']
            print(f"Request calls remailing = {calls_remaning} Tiny calls remailing = {tiny_calls_remaning}")
        except:
            print("move on")

        #Return the key only if there are calls remainig
        if (int(calls_remaning) > 0):
            return key

    return None

'''
getRecipeByUrl : query spoonacular API with the link
Return: Return the request
'''
def getRecipeByUrl(url):
    #Add payload
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
cuisine: string
ingredients: list
Return: Return the request'''
def getRecipes(recipe_links):

    recipe_list = []
    info = {}

    #make a API call and get the recipe
    for link in recipe_links[0:3]:
        result = getRecipeByUrl(link)
        # print(result.json())

        if(result):
        #store the information
            try:
                info = {'title': result.json()['title'],
                        'sourceUrl': result.json()['sourceUrl'],
                        'cookingMinutes': result.json()['cookingMinutes'],
                        'preparationMinutes': result.json()['preparationMinutes'],
                        'image': result.json()['image'],
                        'instructions': result.json()['instructions'],
                        'ingredients' : [key['originalString'] for key in result.json()['extendedIngredients']]
                        }
            except:
                # pass
                print("Recipe not found")

            recipe_list.append(info)
            # print(recipe_list)

    return recipe_list

'''
getLinksFromcsv
return the list of recepies
'''
def getLinksFromcsv(cuisine="Indian", ingredients=[]):
    #make everything lower case
    ingredients= [x.lower().strip() for x in ingredients]
    cuisine = cuisine.lower().strip()

    #get the ingredients whoes recipes we have saved
    df = pd.read_csv(os.path.join('recipes', 'recipes.csv'), skipinitialspace=True)
    df.columns = map(str.lower, df.columns)
    df.dropna(inplace=True)

    #get the synonyms and append to ingredients
    syn_df = pd.read_csv(os.path.join('recipes', 'synonyms.csv'), skipinitialspace=True)
    syn_df.columns = map(str.lower, syn_df.columns)
    syn_df.dropna(inplace=True)
    # print(syn_df)

    #if syninym found append to ingredient
    for ingredient in ingredients:
        try:
            ingredients.extend(syn_df[ingredient].tolist())
        except:
            pass
    print(ingredients)
    # print(df[cuisine].str.contains(ingredient))

    recipe_links_list = []
    for ingredient in ingredients:
        new_list = []
        #find the recipes
        try:
            new_list = df[cuisine][df[cuisine].str.contains(ingredient)].tolist()
        except:
            print("not found")

        recipe_links_list = [x for x in itertools.chain.from_iterable(itertools.zip_longest(recipe_links_list,new_list)) if x]

    print(recipe_links_list)
    return recipe_links_list


# getLinksFromcsv('Mexican', ['tomato'])

'''
getdict()
Testing
'''
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
    'image': 'https://hebbarskitchen.com/wp-content/uploads/mainPhotos/onion-tomato-chutney-recipe-tomato-onion-chutney-recipe-1.jpeg',
    'instructions': 'Instructionsfirstly, in a large tawa heat 1 tsp butter and saute 2 tbsp onion.',
    'ingredients': ['1 tsp butter', '2 tbsp onion finely chopped', '1 cup palak / spinach finely chopped']}]
