from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shops", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="coffeeshop",
            name="rating_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
