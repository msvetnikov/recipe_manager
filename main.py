import os
import json

recipes = []

if os.path.exists('recipes.json'):
    with open('recipes.json', 'r', encoding='utf-8') as f:
        try:
            recipes = json.load(f)
        except json.JSONDecodeError:
            # Если файл оказался пустым или «битым»,
            #  мы просто говорим: «Окей, пусть список будет пустым»
            recipes = []

class RecipeNotFoundError(Exception):
    pass
class InvalidRecipeError(Exception):
    pass
class InvalidCookingTimeError(Exception):
    pass

def create_recipe(recipe: dict):

    # Валидация
    if 'title' not in recipe:
        raise InvalidRecipeError
    if recipe['time'] <= 0:
        raise InvalidCookingTimeError

    # Проверяем пустой ли recipes
    if recipes:
        new_id = recipes[-1]['id'] + 1
    else:
        new_id = 1

    new_recipe = {"id": new_id, **recipe}
    recipes.append(new_recipe)

    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=4)

    print(f'Рецепт успешно создан. ID: {new_id}')
    return new_id

def get_recipe_by_id(target_id: int):
    for recipe in recipes:
        if recipe['id'] == target_id:
            print('Рецепт найден')
            return recipe
    raise RecipeNotFoundError(f'ID {target_id} не существует(')

def filter_by_time(max_time: int):
    approve_recipes = []
    for recipe in recipes:
        if recipe['time'] <= max_time:
            approve_recipes.append(recipe)

    if approve_recipes == []:
        return 'Нет подходящих рецептов'
    
    return approve_recipes

recipe1 = {
    'title': 'Ночная овсянка',
    'ingredients': {'Овсянка': 70, 'Творожок': 100, 'Молоко': 100},
    'instructions': 'Тут инструкция',
    'time': 5
}

try:
    create_recipe(recipe1)
except InvalidRecipeError:
    print('Некорректный рецепт')
except InvalidCookingTimeError:
    print('Время приготовления должно быть > 0 минут')
