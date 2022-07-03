from googlesearch import search
import pandas as pd


def allrecipes_search(dish):
    query = '"site:allrecipes.com": ' + dish
    url = None

    for x in search(query, safe='on', num=1, stop=1, pause=2):
        url = x

    if url is None:
        return 'That is not the kind of thing that I would have a recipe for.'

    return url


def cook_temp(meat):
    df = pd.read_csv(r'C:\Users\Ian\PycharmProjects\DiscBots\BeepBoopBot\temps.csv')
    meat = meat.upper()
    if meat in df['MEAT'].tolist():
        z = df.loc[df['MEAT'] == meat.upper()]
    else:
        return 'Try again with a new meat.'
    return str(z.iat[0, 0]).lower().capitalize() + ' should be cooked to ' + str(z.iat[0, 1]) + 'F.'
