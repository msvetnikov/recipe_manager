import os
import json

class RecipeNotFoundError(Exception):
    pass


class InvalidRecipeError(Exception):
    pass


class InvalidCookingTimeError(Exception):
    pass


class JsonSerializableMixin:
    def to_dict(self) -> dict:
        clean_dict = {}

        for key, value in self.__dict__.items():
            clean_key = key.lstrip('_')
            clean_dict[clean_key] = value

        return clean_dict
    
    def to_json(self) -> str:
        json_string = json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
        return json_string
    

class Recipe(JsonSerializableMixin):
    def __init__(self, title: str, instructions: str, time: int, ingredients: dict | None = None, id: int | None = None):
        self.title = title
        self.time = time
        self.instructions = instructions
        self._id = id
        if ingredients is None:
            self.ingredients = {}
        else:
            self.ingredients = ingredients
    
    @property
    def time(self) -> int:
        return self._time

    @property
    def id(self) -> int | None:
        return self._id

    @time.setter
    def time(self, new_time: int):
        if new_time <= 0:
            raise InvalidCookingTimeError("Время должно быть больше нуля!")
        self._time = new_time


    def __repr__(self):
        return f"Recipe(id={self._id}, title='{self.title}', time={self._time})"

    def __str__(self):
        return (
        f"ID рецепта: {self._id}\n"
        f"Название рецепта: {self.title}\n"
        f"Время приготовления: {self._time} мин.\n"
        f"Необходимые ингредиенты: {self.ingredients}\n"
        f"Инструкция приготовления: {self.instructions}"
    )

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.title == other.title and self._time == other._time
    
    def __hash__(self):
        return hash((self.title, self._time))


class VideoRecipe(Recipe):
    def __init__(self, title, instructions, time, video_url, ingredients = None, id = None):
        super().__init__(title, instructions, time, ingredients, id)
        self.video_url = video_url
    
    def __str__(self):
        last_text = super().__str__()
        new_text = last_text + f"\nСсылка на видео-инструкцию: {self.video_url}"
        return new_text

class RecipeBook:
    _recipes_storage = []

    @classmethod
    def _save_to_file(cls):
        # список объектов класса -> список словарей -> json
        recipes_to_json = []
        for r in cls._recipes_storage:
            recipes_to_json.append(r.to_dict())

        with open('recipes.json', 'w', encoding='utf-8') as f:
            json.dump(recipes_to_json, f, ensure_ascii=False, indent=4)

    @classmethod
    def load_recipes(cls):
        if os.path.exists('recipes.json'):
            try:
                with open('recipes.json', 'r', encoding='utf-8') as raw_data:
                    load_json_recipes = json.load(raw_data)
                    
                    # Очищаем список перед загрузкой, чтобы избежать дубликатов
                    cls._recipes_storage = []
                    
                    for recipe_dict in load_json_recipes:
                        # Проверяем «маркер» видео-рецепта
                        if 'video_url' in recipe_dict:
                            recipe_obj = VideoRecipe(**recipe_dict)
                        else:
                            recipe_obj = Recipe(**recipe_dict)
                            
                        cls._recipes_storage.append(recipe_obj)
            except json.JSONDecodeError:
                print('Битый json')

    @classmethod
    def create_recipe(cls, recipe: Recipe):
        # Валидация
        if not recipe.title.strip():
            raise InvalidRecipeError
        
        # Определение ID рецепта
        if cls._recipes_storage:
            recipe._id = cls._recipes_storage[-1].id + 1
        else:
            recipe._id = 1

        # Добавление в локальный список рецептов
        cls._recipes_storage.append(recipe)

        # Сохранение в recipes.json
        cls._save_to_file()
        print(f'Рецепт "{recipe.title}" успешно сохранен!')
    
    @classmethod
    def update_recipe(cls, target_id: int, new_title: str = None, new_time: int = None):
        recipe = cls.get_recipe_by_id(target_id)
        
        if new_title is not None:
            if not new_title.strip():
                raise InvalidRecipeError("Название не может быть пустым!")
            recipe.title = new_title
            
        if new_time is not None:
            recipe.time = new_time  # Включается @time.setter с валидацией!
            
        cls._save_to_file()
        print(f'Рецепт с ID {target_id} успешно обновлен!')

    @classmethod
    def delete_recipe(cls, target_id: int):
        # Переиспользуем логику поиска. Если ID нет, сработает исключение
        recipe = cls.get_recipe_by_id(target_id)
        
        cls._recipes_storage.remove(recipe)
        cls._save_to_file()
        print(f'Рецепт с ID {target_id} ("{recipe.title}") успешно удален!')
    
    @classmethod
    def print_all_recipes(cls):
        if not cls._recipes_storage:
            print("Книга рецептов пуста.")
            return
            
        print("\n=== ВСЕ РЕЦЕПТЫ В КНИГЕ ===")
        for recipe in cls._recipes_storage:
            print(recipe)  # ПОЛИМОРФИЗМ! Python сам выберет нужный __str__
            print("-" * 30)

    @classmethod
    def get_recipe_by_id(cls, target_id: int):
        for recipe in cls._recipes_storage:
            if recipe.id == target_id:
                print('Рецепт найден')
                return recipe
        raise RecipeNotFoundError(f'ID {target_id} не существует')

    @classmethod
    def filter_by_time(cls, max_time: int):
        approve_recipes = []
        for recipe in cls._recipes_storage:
            if recipe.time <= max_time:
                approve_recipes.append(recipe)
        return approve_recipes