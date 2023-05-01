from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Кастомная команда загрузки данных об ингредиентах из csv файла в БД."""

    help = 'Загрузка данных ингредиентов из csv файла в БД.'

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            print('Данные инредиентов уже загружены!')

            return

        print('Загрузка данных ингредиентов в БД ...')

        bulk_data = []
        for row in DictReader(
                open('ingredients.csv', encoding='utf-8'),
                fieldnames=('name', 'measurement_unit')):
            bulk_data.append(Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit'],
            ))

        Ingredient.objects.bulk_create(bulk_data)
