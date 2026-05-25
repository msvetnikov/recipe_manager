import os
import json

class RecipeNotFoundError(Exception):
    pass
class InvalidRecipeError(Exception):
    pass
class InvalidCookingTimeError(Exception):
    pass


class Recipe:
    def __init__(self, title: str, instructions: str, time: int, ingredients: dict | None = None, id: int | None = None):
        self.title = title
        self.time = time
        self.instructions = instructions
        self.id = id
        if ingredients is None:
            self.ingredients = {}
        else:
            self.ingredients = ingredients
    
    def __repr__(self):
        return f"Recipe(id={self.id}, title='{self.title}', time={self.time})"

    def __str__(self):
        return (
        f"ID рецепта: {self.id}\n"
        f"Название рецепта: {self.title}\n"
        f"Время приготовления: {self.time} мин.\n"
        f"Необходимые ингредиенты: {self.ingredients}\n"
        f"Инструкция приготовления: {self.instructions}"
    )

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        
        return self.title == other.title and self.time == other.time
    
    def __hash__(self):
        return hash((self.title, self.time))


def load_recipes():
    recipes = []
    if os.path.exists('recipes.json'):
        try:
            with open('recipes.json', 'r', encoding='utf-8') as raw_data:
                load_json_recipes = json.load(raw_data)
                for recipe in load_json_recipes:
                    recipe1 = Recipe(**recipe)
                    recipes.append(recipe1)
        except json.JSONDecodeError:
            print('Битый json')
    return recipes
recipes = load_recipes()


def create_recipe(recipe: Recipe):

    # Валидация
    if not recipe.title.strip(): # if not True = False / if not False = True
        raise InvalidRecipeError
    if recipe.time <= 0:
        raise InvalidCookingTimeError
    
    # Определение ID рецепта
    if recipes:
        recipe.id = recipes[-1].id + 1
    else:
        recipe.id = 1

    # Добавление в локальный список рецептов
    recipes.append(recipe)

    # Превращаем список объектов класса в список в словарей
    recipes_to_json = []
    for r in recipes:
        recipes_to_json.append(r.__dict__)
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes_to_json, f, ensure_ascii=False, indent=4)
    
    print(f'Рецепт "{recipe.title}" успешно сохранен!')


def get_recipe_by_id(target_id: int):
    for recipe in recipes:
        if recipe.id == target_id:
            print('Рецепт найден')
            return recipe
    raise RecipeNotFoundError(f'ID {target_id} не существует')


def filter_by_time(max_time: int):
    approve_recipes = []
    for recipe in recipes:
        if recipe.time <= max_time:
            approve_recipes.append(recipe)
    return approve_recipes
    
