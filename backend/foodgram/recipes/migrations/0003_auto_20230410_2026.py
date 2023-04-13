# Generated by Django 2.2.16 on 2023-04-10 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipes_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientsforrecipes',
            name='ingredient_id',
        ),
        migrations.RemoveField(
            model_name='ingredientsforrecipes',
            name='recipe_id',
        ),
        migrations.AddField(
            model_name='ingredientsforrecipes',
            name='ingredient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipes_for_ingredients', to='recipes.Ingredients', verbose_name='id ингредиента'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredientsforrecipes',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_for_recipe', to='recipes.Recipes', verbose_name='id рецепта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientsForRecipes', to='recipes.Ingredients'),
        ),
    ]
