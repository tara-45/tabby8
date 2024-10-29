# Partially generated by Django 3.2.3 on 2021-10-15 06:07, but mostly written manually because this
# is a field renaming.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0010_merge_20210919_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ballotsubmission',
            old_name='partial',
            new_name='single_adj',
        ),
        migrations.AlterField(
            model_name='ballotsubmission',
            name='single_adj',
            field=models.BooleanField(default=False, help_text='Whether this submission represents only the submitting adjudicator on a panel, when individual adjudicator ballots are enabled.', verbose_name='single adjudicator'),
        ),
    ]
