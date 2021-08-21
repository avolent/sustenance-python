import os
import ast
import random 
import numpy as np
from collections import Counter
import json
import requests

# path = os.path.dirname(os.path.realpath(__file__)) + "\\"
# file = open(path + "recipes.txt", "r")
# contents = file.read()
contents = requests.get("https://drive.google.com/u/0/uc?id=1RQ7F36ZA_lY7t0jU4xmLi37gN-W6KBXX&export=download").text
dictionary = ast.literal_eval(contents)
# file.close()

# meal_count = int(input("How many meals are your planning for? "))
meal_count = 5
recipes_count = len(dictionary)
meal_names = list(dictionary.keys())
meal_values = list(dictionary.values())
meal_selection = np.random.permutation(recipes_count)[:meal_count]

shoppinglist = {}
meallist = []
data = { "value1" : "", "value2" : "", "value3" : "" }

for meal in meal_selection:
    selection = meal_names[meal]
    meallist.append(selection)
    data["value1"] = data["value1"] + "<li>" + selection + "</li>"

print("\nRandomly Selected Meals:")
for item in meallist:
    print(item)

for meal in meal_selection:
    ingredients = meal_values[meal]
    shoppinglist = dict(Counter(shoppinglist) + Counter(ingredients))
    
print("\nHere is your shopping list!\n---------------------------")
for key in shoppinglist:
    print(f"{shoppinglist[key]} {key}")
    data["value2"] = data["value2"] + "<li>" + str(shoppinglist[key]) + " " + str(key) + "</li>" 


# Set the webhook_url to the one provided by ifttt when you create the webhook. https://maker.ifttt.com/trigger/<event_name>/with/key/<unique_ifttt_code>
webhook_url = 'https://maker.ifttt.com/trigger/shopping/with/key/<unique_ifttt_code>'

# print(data)

response = requests.post(
    webhook_url, data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to ifttt returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )