from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='final_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='promo_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
