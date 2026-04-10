# Generated migration for adding agent field to Shop model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # Adjust if needed based on your accounts migrations
        ('shops', '0013_controlfrequency_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='agent',
            field=models.ForeignKey(
                blank=True,
                help_text='Agent qui suit cette boutique',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='managed_shops',
                to='accounts.account'
            ),
        ),
    ]

