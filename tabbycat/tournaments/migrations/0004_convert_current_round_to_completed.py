# Generated by Django 2.0.8 on 2018-08-26 00:38

from django.db import migrations


def convert_current_round_to_completed(apps, schema_editor):

    Tournament = apps.get_model('tournaments', 'Tournament')  # noqa: N806

    for tournament in Tournament.objects.all():
        if tournament.current_round is None:
            continue
        now = tournament.current_round.seq
        tournament.round_set.filter(seq__lt=now).update(completed=True)
        tournament.round_set.filter(seq__gte=now).update(completed=False)


def convert_completed_to_current_round(apps, schema_editor):

    Tournament = apps.get_model('tournaments', 'Tournament')  # noqa: N806

    for tournament in Tournament.objects.all():
        if tournament.current_round is not None:
            continue
        tournament.current_round = tournament.round_set.filter(completed=False).order_by('seq').first()
        tournament.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_round_completed'),
    ]

    operations = [
        migrations.RunPython(convert_current_round_to_completed,
            convert_completed_to_current_round,
            elidable=True),
    ]
