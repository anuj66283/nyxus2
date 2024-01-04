# Generated by Django 5.0 on 2024-01-02 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0008_reviews_wishlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkout",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
        migrations.RemoveField(
            model_name="checkout",
            name="book",
        ),
        migrations.AddField(
            model_name="checkout",
            name="book",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="book.books"
            ),
        ),
    ]
