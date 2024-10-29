# Generated by Django 2.0.8 on 2018-10-20 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adjallocation', '0007_preformedpanel_preformedpaneladjudicator'),
    ]

    operations = [
        migrations.AddField(
            model_name='preformedpanel',
            name='bracket_max',
            field=models.FloatField(default=0, help_text='Estimate of the highest bracket for which this panel might be', verbose_name='maximum bracket'),
        ),
        migrations.AddField(
            model_name='preformedpanel',
            name='bracket_min',
            field=models.FloatField(default=0, help_text='Estimate of the lowest bracket for which this panel might be', verbose_name='minimum bracket'),
        ),
        migrations.AddField(
            model_name='preformedpanel',
            name='liveness',
            field=models.IntegerField(default=0, help_text='Number of categories this room is expected to be live for', verbose_name='liveness'),
        ),
        migrations.AddField(
            model_name='preformedpanel',
            name='room_rank',
            field=models.IntegerField(default=0, help_text='Sequential number of panel, not used in any algorithms', verbose_name='room rank'),
        ),
    ]
