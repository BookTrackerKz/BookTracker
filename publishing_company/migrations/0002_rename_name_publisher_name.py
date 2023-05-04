

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishing_company', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publisher',
            old_name='Name',
            new_name='name',
        ),
    ]
