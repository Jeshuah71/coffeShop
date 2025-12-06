from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journalentry",
            name="my_rating",
            field=models.DecimalField(max_digits=3, decimal_places=1),
        ),
    ]
