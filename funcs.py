from googlesearch import search
import pandas as pd
import requests
from bs4 import BeautifulSoup
from joblib import load


# Returns the top search results from allrecipes.com for a queried dish.
def allrecipes_search(dish):
    query = '"site:allrecipes.com": ' + dish
    url = None

    for x in search(query, safe='on', num=1, stop=1, pause=2):
        url = x

    if url is None:
        return 'That is not the kind of thing that I would have a recipe for.'

    return url


# Returns cook temperatures of given meats from an external file.
def cook_temp(meat):
    df = pd.read_csv(r'C:\Users\Ian\PycharmProjects\DiscBots\BeepBoopBot\temps.csv')
    meat = meat.upper()
    if meat in df['MEAT'].tolist():
        z = df.loc[df['MEAT'] == meat.upper()]
    else:
        return 'Try again with a new meat.'
    return str(z.iat[0, 0]).lower().capitalize() + ' should be cooked to ' + str(z.iat[0, 1]) + 'F.'


# Gets the webpage and parses with BeautifulSoup. Returns a list of ingredients.
def get_ingredients(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(class_='recipe-content-container')
    ingredient_section = results.find('ul', class_='ingredients-section')

    ingredients = [ingredient.text.strip() for ingredient in ingredient_section if ingredient.text.strip()]

    ingredients = ['Ingredients:'] + ingredients

    return ingredients


# Gets the webpage and parses with BeautifulSoup. Returns a list of directions.
def get_directions(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(class_='recipe-content-container')
    instructions_section = results.find('ul', class_='instructions-section')

    directions = [step.text.strip() for step in instructions_section if step.text.strip()]

    # Removes the word "Advertisement" from the list of directions, if present.
    for x in range(len(directions)):
        if directions[x][-13:] == 'Advertisement':
            directions[x] = directions[x][:-13].strip()

    directions = ['Directions:'] + directions

    return directions


# Returns the isolated instructions from a given URL, provided that it is valid.
def isolate_instructions(url):
    try:
        ingredients = get_ingredients(url)
        directions = get_directions(url)

    except:
        return ['Error: unable to isolate ingredients and directions. '
                'Please ensure you use a recipe page from allrecipes.com']

    return ingredients + directions


# Checks to make sure an argument is within a certain range. If not, prepares a corrective message to send.
# Also imputes 'na' entries with appropriate metrics.
def check_flag(attr, arg, lower=0, upper=1, binary=False):
    if arg == 'na':
        imp_vals = load('saved_fill_values.joblib')
        return 'fill', imp_vals[attr]

    if binary:
        if arg not in ('0', '1'):
            return 'fail', 'Please check your entry for ' + attr + ' and try again.'
        return 'pass'

    arg = float(arg)
    if not lower <= arg <= upper:
        return 'fail', 'Please check your value of ' + str(arg) + ' and try again.'
    return 'pass'


# Classifies milk quality via a previously-trained sklearn model.
def milk_predict(variables):
    variables = [float(x) for x in variables]
    mod_test = load('saved_model.joblib')
    return mod_test.predict([variables])
